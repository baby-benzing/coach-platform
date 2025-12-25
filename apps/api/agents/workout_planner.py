"""
Workout Planning Agent

A multi-step agentic workflow for generating personalized, periodized
training plans based on client assessments and coach preferences.

Uses the Anthropic API with tool use for a structured planning process.
"""

import anthropic
import json
from typing import Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

from config import get_settings
from .prompts import get_full_system_prompt, STEP_PROMPTS
from .tools import WORKOUT_PLANNING_TOOLS, execute_tool, EXERCISE_DATABASE


@dataclass
class AgentContext:
    """Context maintained across agent steps."""
    client_assessment: dict = field(default_factory=dict)
    fms_analysis: Optional[dict] = None
    selected_exercises: list = field(default_factory=list)
    weekly_structure: Optional[dict] = None
    workout_plan: Optional[dict] = None
    conversation_history: list = field(default_factory=list)
    step_outputs: dict = field(default_factory=dict)


@dataclass
class AgentStep:
    """Represents a step in the agent workflow."""
    name: str
    prompt_template: str
    required_tools: list = field(default_factory=list)
    max_iterations: int = 5


class WorkoutPlanningAgent:
    """
    Multi-step agent for creating periodized training plans.

    The agent follows a structured workflow:
    1. Analyze client assessment (FMS, goals, availability)
    2. Select appropriate exercises from library
    3. Design weekly training structure
    4. Generate complete 4-week plan
    5. Review and refine for safety/effectiveness
    """

    def __init__(self, coach_philosophy: str = ""):
        settings = get_settings()
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = "claude-sonnet-4-20250514"
        self.system_prompt = get_full_system_prompt(coach_philosophy)
        self.context = AgentContext()
        self.exercise_database = EXERCISE_DATABASE

    def set_exercise_database(self, exercises: list[dict]):
        """
        Set custom exercise database from Supabase.

        Args:
            exercises: List of exercise dicts from database
        """
        # Convert flat list to categorized structure
        categorized = {}
        for ex in exercises:
            category = ex.get("category", "strength")
            if category not in categorized:
                categorized[category] = {"beginner": [], "intermediate": [], "advanced": []}

            # Determine difficulty from tags or default to intermediate
            difficulty = "intermediate"
            tags = ex.get("manual_tags", []) + ex.get("ai_tags", [])
            if any("beginner" in t.lower() for t in tags):
                difficulty = "beginner"
            elif any("advanced" in t.lower() for t in tags):
                difficulty = "advanced"

            categorized[category][difficulty].append({
                "name": ex.get("name"),
                "equipment": ex.get("equipment", []),
                "cues": ex.get("description", "").split(". ")[:3],
                "youtube_url": ex.get("youtube_url")
            })

        self.exercise_database = categorized

    async def generate_plan(
        self,
        assessment: dict,
        coach_preferences: dict,
        exercises: Optional[list[dict]] = None
    ) -> dict:
        """
        Generate a complete workout plan from assessment data.

        Args:
            assessment: Client assessment data including FMS scores
            coach_preferences: Coach's training preferences
            exercises: Optional custom exercise library

        Returns:
            Complete workout plan dict
        """
        # Initialize context
        self.context = AgentContext(client_assessment=assessment)

        if exercises:
            self.set_exercise_database(exercises)

        # Run the multi-step workflow
        steps = [
            AgentStep(
                name="analyze_assessment",
                prompt_template=STEP_PROMPTS["analyze_assessment"],
                required_tools=["analyze_fms_scores"]
            ),
            AgentStep(
                name="select_exercises",
                prompt_template=STEP_PROMPTS["select_exercises"],
                required_tools=["query_exercise_library", "check_exercise_compatibility"]
            ),
            AgentStep(
                name="design_weekly_structure",
                prompt_template=STEP_PROMPTS["design_weekly_structure"].format(
                    days_per_week=assessment.get("availability", {}).get("days_per_week", 3),
                    minutes_per_session=assessment.get("availability", {}).get("minutes_per_session", 60)
                ),
                required_tools=["calculate_training_volume"]
            ),
            AgentStep(
                name="generate_full_plan",
                prompt_template=STEP_PROMPTS["generate_full_plan"],
                required_tools=["generate_workout_day", "save_workout_plan"]
            ),
            AgentStep(
                name="review_and_refine",
                prompt_template=STEP_PROMPTS["review_and_refine"],
                required_tools=["check_exercise_compatibility", "save_workout_plan"]
            )
        ]

        for step in steps:
            await self._execute_step(step, assessment, coach_preferences)

        return self._extract_final_plan()

    async def _execute_step(
        self,
        step: AgentStep,
        assessment: dict,
        coach_preferences: dict
    ):
        """Execute a single step of the workflow."""
        print(f"\n{'='*50}")
        print(f"Step: {step.name}")
        print(f"{'='*50}")

        # Build the prompt with context
        prompt = self._build_step_prompt(step, assessment, coach_preferences)

        # Add to conversation history
        self.context.conversation_history.append({
            "role": "user",
            "content": prompt
        })

        # Run agent loop for this step
        iteration = 0
        while iteration < step.max_iterations:
            iteration += 1

            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=self.system_prompt,
                tools=WORKOUT_PLANNING_TOOLS,
                messages=self.context.conversation_history
            )

            # Process response
            assistant_content = []
            tool_results = []

            for block in response.content:
                if block.type == "text":
                    print(f"\nAgent: {block.text[:500]}...")
                    assistant_content.append({"type": "text", "text": block.text})

                elif block.type == "tool_use":
                    print(f"\nTool Call: {block.name}")
                    print(f"Input: {json.dumps(block.input, indent=2)[:200]}...")

                    # Execute the tool
                    result = execute_tool(
                        block.name,
                        block.input,
                        {"exercises": self.exercise_database}
                    )

                    print(f"Result: {json.dumps(result, indent=2)[:200]}...")

                    assistant_content.append({
                        "type": "tool_use",
                        "id": block.id,
                        "name": block.name,
                        "input": block.input
                    })

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result)
                    })

                    # Update context based on tool results
                    self._update_context(block.name, result)

            # Add assistant response to history
            self.context.conversation_history.append({
                "role": "assistant",
                "content": assistant_content
            })

            # If there were tool calls, add results and continue
            if tool_results:
                self.context.conversation_history.append({
                    "role": "user",
                    "content": tool_results
                })
            else:
                # No more tool calls, step is complete
                break

            # Check stop reason
            if response.stop_reason == "end_turn":
                break

        # Save step output
        self.context.step_outputs[step.name] = {
            "iterations": iteration,
            "final_response": response.content[-1].text if response.content else ""
        }

    def _build_step_prompt(
        self,
        step: AgentStep,
        assessment: dict,
        coach_preferences: dict
    ) -> str:
        """Build the prompt for a step including relevant context."""
        prompt_parts = [step.prompt_template]

        # Add assessment data for first step
        if step.name == "analyze_assessment":
            prompt_parts.append(f"\n\n## Client Assessment Data\n```json\n{json.dumps(assessment, indent=2)}\n```")

        # Add coach preferences
        if coach_preferences:
            prompt_parts.append(f"\n\n## Coach Preferences\n```json\n{json.dumps(coach_preferences, indent=2)}\n```")

        # Add previous analysis for later steps
        if step.name != "analyze_assessment" and self.context.fms_analysis:
            prompt_parts.append(f"\n\n## FMS Analysis (from previous step)\n```json\n{json.dumps(self.context.fms_analysis, indent=2)}\n```")

        return "\n".join(prompt_parts)

    def _update_context(self, tool_name: str, result: dict):
        """Update agent context based on tool results."""
        if tool_name == "analyze_fms_scores":
            self.context.fms_analysis = result

        elif tool_name == "query_exercise_library":
            if "exercises" in result:
                self.context.selected_exercises.extend(result["exercises"])

        elif tool_name == "save_workout_plan":
            if "plan" in result:
                self.context.workout_plan = result["plan"]

    def _extract_final_plan(self) -> dict:
        """Extract the final workout plan from context."""
        if self.context.workout_plan:
            return self.context.workout_plan

        # Fallback: construct plan from context
        assessment = self.context.client_assessment
        availability = assessment.get("availability", {})
        days_per_week = availability.get("days_per_week", 3)

        # Generate basic plan structure
        workout_days = []
        focus_rotation = ["Upper Body", "Lower Body", "Full Body", "Cardio/Active Recovery"]

        for week in range(1, 5):
            phase = self._get_phase_for_week(week)

            for day in range(days_per_week):
                day_of_week = availability.get("preferred_days", ["Monday", "Wednesday", "Friday"])[day % 3]
                day_index = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"].index(day_of_week) if day_of_week in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"] else day + 1

                focus = focus_rotation[day % len(focus_rotation)]

                workout_day = {
                    "week_number": week,
                    "day_of_week": day_index,
                    "name": f"Week {week} - {day_of_week}",
                    "focus": focus,
                    "exercises": self._generate_exercises_for_focus(focus, phase),
                    "notes": f"Phase: {phase}. Focus on movement quality."
                }
                workout_days.append(workout_day)

        return {
            "name": f"4-Week Personalized Training Plan",
            "weeks": 4,
            "workout_days": workout_days,
            "coach_notes": "Plan generated by AI coach. Review and adjust as needed based on client feedback."
        }

    def _get_phase_for_week(self, week: int) -> str:
        """Get the training phase for a given week."""
        if week <= 2:
            return "anatomical_adaptation"
        elif week == 3:
            return "hypertrophy"
        else:
            return "strength"

    def _generate_exercises_for_focus(self, focus: str, phase: str) -> list:
        """Generate exercises for a specific focus and phase."""
        phase_params = {
            "anatomical_adaptation": {"sets": 3, "reps": "12-15", "rpe": 6, "rest": 60},
            "hypertrophy": {"sets": 4, "reps": "8-12", "rpe": 7, "rest": 90},
            "strength": {"sets": 4, "reps": "5-8", "rpe": 8, "rest": 120}
        }
        params = phase_params.get(phase, phase_params["hypertrophy"])

        exercises = []

        if "Upper" in focus:
            exercises = [
                {"exercise_name": "Push-Up or Bench Press", "sets": params["sets"], "reps": params["reps"], "rest_seconds": params["rest"], "rpe": params["rpe"]},
                {"exercise_name": "Dumbbell Row", "sets": params["sets"], "reps": params["reps"], "rest_seconds": params["rest"], "rpe": params["rpe"]},
                {"exercise_name": "Shoulder Press", "sets": 3, "reps": params["reps"], "rest_seconds": 60, "rpe": params["rpe"]},
                {"exercise_name": "Face Pull", "sets": 3, "reps": "12-15", "rest_seconds": 45, "rpe": 6},
            ]
        elif "Lower" in focus:
            exercises = [
                {"exercise_name": "Squat Variation", "sets": params["sets"], "reps": params["reps"], "rest_seconds": params["rest"], "rpe": params["rpe"]},
                {"exercise_name": "Romanian Deadlift", "sets": params["sets"], "reps": params["reps"], "rest_seconds": params["rest"], "rpe": params["rpe"]},
                {"exercise_name": "Split Squat", "sets": 3, "reps": "10-12 each", "rest_seconds": 60, "rpe": params["rpe"]},
                {"exercise_name": "Glute Bridge", "sets": 3, "reps": "12-15", "rest_seconds": 45, "rpe": 6},
            ]
        elif "Cardio" in focus:
            exercises = [
                {"exercise_name": "Zone 2 Cardio", "duration_minutes": 30, "target_hr": 130, "notes": "Conversational pace"},
            ]
        else:  # Full Body
            exercises = [
                {"exercise_name": "Goblet Squat", "sets": params["sets"], "reps": params["reps"], "rest_seconds": params["rest"], "rpe": params["rpe"]},
                {"exercise_name": "Push-Up", "sets": 3, "reps": params["reps"], "rest_seconds": 60, "rpe": params["rpe"]},
                {"exercise_name": "Dumbbell Row", "sets": 3, "reps": params["reps"], "rest_seconds": 60, "rpe": params["rpe"]},
                {"exercise_name": "Plank", "sets": 3, "reps": "30-45 sec", "rest_seconds": 45, "rpe": 6},
            ]

        return exercises


# Synchronous wrapper for use in FastAPI
def generate_workout_plan_sync(
    assessment: dict,
    coach_preferences: dict,
    coach_philosophy: str = "",
    exercises: Optional[list[dict]] = None
) -> dict:
    """
    Synchronous wrapper for workout plan generation.

    For use in FastAPI endpoints that don't need async.
    """
    import asyncio

    agent = WorkoutPlanningAgent(coach_philosophy=coach_philosophy)

    # Run async function in event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(
            agent.generate_plan(assessment, coach_preferences, exercises)
        )
        return result
    finally:
        loop.close()
