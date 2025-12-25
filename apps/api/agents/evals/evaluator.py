"""
Evaluation framework for workout planning agent.

Provides structured evaluation of generated workout plans against
expected characteristics and safety criteria.
"""

import json
from dataclasses import dataclass, field
from typing import Any, Optional
from enum import Enum


class EvaluationCriteria(Enum):
    """Evaluation criteria for workout plans."""
    SAFETY = "safety"
    APPROPRIATENESS = "appropriateness"
    PROGRESSION = "progression"
    VOLUME = "volume"
    EXERCISE_SELECTION = "exercise_selection"
    STRUCTURE = "structure"
    GOAL_ALIGNMENT = "goal_alignment"


@dataclass
class CriterionResult:
    """Result for a single evaluation criterion."""
    criterion: EvaluationCriteria
    passed: bool
    score: float  # 0-1
    details: str
    issues: list = field(default_factory=list)


@dataclass
class EvaluationResult:
    """Complete evaluation result for a workout plan."""
    test_case_name: str
    overall_passed: bool
    overall_score: float
    criterion_results: dict = field(default_factory=dict)
    summary: str = ""
    recommendations: list = field(default_factory=list)


class PlanEvaluator:
    """
    Evaluates generated workout plans against expected characteristics.

    Checks for:
    1. Safety - No contraindicated exercises
    2. Appropriateness - Matches client level and limitations
    3. Progression - Logical progression across weeks
    4. Volume - Appropriate sets/reps for experience level
    5. Exercise Selection - Correct movement patterns and alternatives
    6. Structure - Proper plan organization
    7. Goal Alignment - Plan targets stated goals
    """

    def __init__(self):
        self.weight_by_criterion = {
            EvaluationCriteria.SAFETY: 0.25,
            EvaluationCriteria.APPROPRIATENESS: 0.20,
            EvaluationCriteria.GOAL_ALIGNMENT: 0.15,
            EvaluationCriteria.PROGRESSION: 0.15,
            EvaluationCriteria.VOLUME: 0.10,
            EvaluationCriteria.EXERCISE_SELECTION: 0.10,
            EvaluationCriteria.STRUCTURE: 0.05,
        }

    def evaluate(
        self,
        plan: dict,
        test_case: dict
    ) -> EvaluationResult:
        """
        Evaluate a workout plan against expected characteristics.

        Args:
            plan: Generated workout plan
            test_case: Test case with assessment and expected characteristics

        Returns:
            EvaluationResult with detailed scoring
        """
        expected = test_case.get("expected_characteristics", {})
        assessment = test_case.get("assessment", {})

        criterion_results = {}

        # Evaluate each criterion
        criterion_results[EvaluationCriteria.SAFETY] = self._evaluate_safety(
            plan, expected, assessment
        )
        criterion_results[EvaluationCriteria.APPROPRIATENESS] = self._evaluate_appropriateness(
            plan, expected, assessment
        )
        criterion_results[EvaluationCriteria.PROGRESSION] = self._evaluate_progression(
            plan, expected
        )
        criterion_results[EvaluationCriteria.VOLUME] = self._evaluate_volume(
            plan, expected, assessment
        )
        criterion_results[EvaluationCriteria.EXERCISE_SELECTION] = self._evaluate_exercise_selection(
            plan, expected
        )
        criterion_results[EvaluationCriteria.STRUCTURE] = self._evaluate_structure(
            plan, assessment
        )
        criterion_results[EvaluationCriteria.GOAL_ALIGNMENT] = self._evaluate_goal_alignment(
            plan, assessment
        )

        # Calculate overall score
        overall_score = sum(
            result.score * self.weight_by_criterion[criterion]
            for criterion, result in criterion_results.items()
        )

        # Determine if passed (threshold: 0.7)
        overall_passed = overall_score >= 0.7 and all(
            result.passed for criterion, result in criterion_results.items()
            if criterion == EvaluationCriteria.SAFETY
        )

        # Generate recommendations
        recommendations = []
        for criterion, result in criterion_results.items():
            if not result.passed or result.score < 0.8:
                recommendations.extend(result.issues)

        return EvaluationResult(
            test_case_name=test_case.get("name", "Unknown"),
            overall_passed=overall_passed,
            overall_score=overall_score,
            criterion_results={c.value: r for c, r in criterion_results.items()},
            summary=self._generate_summary(overall_score, criterion_results),
            recommendations=recommendations
        )

    def _evaluate_safety(
        self,
        plan: dict,
        expected: dict,
        assessment: dict
    ) -> CriterionResult:
        """Evaluate safety - no contraindicated exercises."""
        issues = []
        should_avoid = expected.get("should_avoid", [])

        all_exercises = self._extract_all_exercises(plan)

        # Check for contraindicated exercises
        for exercise in all_exercises:
            exercise_lower = exercise.lower()
            for avoid in should_avoid:
                if avoid.lower() in exercise_lower:
                    issues.append(f"Contraindicated exercise found: {exercise} (should avoid: {avoid})")

        # Check FMS score implications
        fms = assessment.get("fms_scores", {})
        if fms.get("shoulder_mobility", 3) < 3:
            overhead_exercises = [e for e in all_exercises if "overhead" in e.lower() or "press" in e.lower()]
            if overhead_exercises:
                # Check if it's landmine or floor press (acceptable alternatives)
                for ex in overhead_exercises:
                    if "landmine" not in ex.lower() and "floor" not in ex.lower():
                        issues.append(f"Overhead movement with shoulder mobility limitation: {ex}")

        score = 1.0 - (len(issues) * 0.2)
        score = max(0, score)

        return CriterionResult(
            criterion=EvaluationCriteria.SAFETY,
            passed=len(issues) == 0,
            score=score,
            details=f"Found {len(issues)} safety concerns",
            issues=issues
        )

    def _evaluate_appropriateness(
        self,
        plan: dict,
        expected: dict,
        assessment: dict
    ) -> CriterionResult:
        """Evaluate if plan matches client level and limitations."""
        issues = []
        experience = assessment.get("exercise_history", {}).get("experience_level", "intermediate")

        all_exercises = self._extract_all_exercises(plan)

        # Check for exercises too advanced for level
        advanced_markers = ["weighted", "barbell", "power", "plyometric", "olympic"]
        beginner_exercises = ["goblet", "bodyweight", "machine", "band", "dumbbell"]

        if experience == "beginner":
            for exercise in all_exercises:
                exercise_lower = exercise.lower()
                if any(marker in exercise_lower for marker in advanced_markers):
                    if not any(beg in exercise_lower for beg in beginner_exercises):
                        issues.append(f"Advanced exercise for beginner: {exercise}")

        # Check RPE range
        rpe_range = expected.get("rpe_range", [6, 8])
        workout_days = plan.get("workout_days", [])
        for day in workout_days:
            for ex in day.get("exercises", []):
                rpe = ex.get("rpe", 7)
                if rpe < rpe_range[0] or rpe > rpe_range[1]:
                    issues.append(f"RPE {rpe} outside expected range {rpe_range} for {ex.get('exercise_name', 'exercise')}")

        score = 1.0 - (len(issues) * 0.15)
        score = max(0, score)

        return CriterionResult(
            criterion=EvaluationCriteria.APPROPRIATENESS,
            passed=score >= 0.7,
            score=score,
            details=f"Appropriateness check found {len(issues)} issues",
            issues=issues
        )

    def _evaluate_progression(
        self,
        plan: dict,
        expected: dict
    ) -> CriterionResult:
        """Evaluate logical progression across weeks."""
        issues = []
        workout_days = plan.get("workout_days", [])

        # Group by week
        weeks = {}
        for day in workout_days:
            week = day.get("week_number", 1)
            if week not in weeks:
                weeks[week] = []
            weeks[week].append(day)

        # Check for progression patterns
        if len(weeks) >= 4:
            # Week 1-2 should be lower intensity
            # Week 3 should increase
            # Week 4 should be highest or deload

            week1_avg_rpe = self._get_avg_rpe(weeks.get(1, []))
            week3_avg_rpe = self._get_avg_rpe(weeks.get(3, []))
            week4_avg_rpe = self._get_avg_rpe(weeks.get(4, []))

            if week3_avg_rpe < week1_avg_rpe:
                issues.append("Week 3 intensity lower than Week 1 (should progress)")

        score = 1.0 - (len(issues) * 0.25)
        score = max(0, score)

        return CriterionResult(
            criterion=EvaluationCriteria.PROGRESSION,
            passed=score >= 0.7,
            score=score,
            details=f"Progression check found {len(issues)} issues",
            issues=issues
        )

    def _evaluate_volume(
        self,
        plan: dict,
        expected: dict,
        assessment: dict
    ) -> CriterionResult:
        """Evaluate training volume appropriateness."""
        issues = []
        experience = assessment.get("exercise_history", {}).get("experience_level", "intermediate")

        # Expected weekly sets per muscle group
        expected_sets = {
            "beginner": (8, 14),
            "intermediate": (12, 20),
            "advanced": (16, 28)
        }

        min_sets, max_sets = expected_sets.get(experience, (12, 20))

        # Count total weekly exercises (rough proxy for volume)
        workout_days = plan.get("workout_days", [])
        weeks = {}
        for day in workout_days:
            week = day.get("week_number", 1)
            if week not in weeks:
                weeks[week] = 0
            for ex in day.get("exercises", []):
                sets = ex.get("sets", 3)
                weeks[week] += sets

        for week, total_sets in weeks.items():
            if total_sets < min_sets * 2:  # Rough approximation
                issues.append(f"Week {week} volume may be too low ({total_sets} total sets)")
            elif total_sets > max_sets * 3:
                issues.append(f"Week {week} volume may be too high ({total_sets} total sets)")

        score = 1.0 - (len(issues) * 0.2)
        score = max(0, score)

        return CriterionResult(
            criterion=EvaluationCriteria.VOLUME,
            passed=score >= 0.7,
            score=score,
            details=f"Volume check found {len(issues)} issues",
            issues=issues
        )

    def _evaluate_exercise_selection(
        self,
        plan: dict,
        expected: dict
    ) -> CriterionResult:
        """Evaluate if required exercises are included."""
        issues = []
        should_include = expected.get("should_include", [])

        all_exercises = self._extract_all_exercises(plan)
        all_exercises_lower = [e.lower() for e in all_exercises]

        # Check for required exercises
        for required in should_include:
            found = any(required.lower() in ex for ex in all_exercises_lower)
            if not found:
                issues.append(f"Missing expected exercise/pattern: {required}")

        # Score based on how many required exercises are present
        if should_include:
            found_count = len(should_include) - len(issues)
            score = found_count / len(should_include)
        else:
            score = 1.0

        return CriterionResult(
            criterion=EvaluationCriteria.EXERCISE_SELECTION,
            passed=score >= 0.6,
            score=score,
            details=f"Found {len(should_include) - len(issues)}/{len(should_include)} expected exercises",
            issues=issues
        )

    def _evaluate_structure(
        self,
        plan: dict,
        assessment: dict
    ) -> CriterionResult:
        """Evaluate plan structure and organization."""
        issues = []

        workout_days = plan.get("workout_days", [])
        availability = assessment.get("availability", {})
        expected_days = availability.get("days_per_week", 3)
        expected_weeks = 4

        # Check week count
        weeks = set(d.get("week_number", 1) for d in workout_days)
        if len(weeks) < expected_weeks:
            issues.append(f"Only {len(weeks)} weeks found, expected {expected_weeks}")

        # Check days per week
        for week in weeks:
            week_days = [d for d in workout_days if d.get("week_number") == week]
            if len(week_days) < expected_days:
                issues.append(f"Week {week} has {len(week_days)} days, expected {expected_days}")

        # Check for required fields
        for day in workout_days:
            if not day.get("focus"):
                issues.append(f"Missing focus for {day.get('name', 'workout')}")
            if not day.get("exercises"):
                issues.append(f"No exercises in {day.get('name', 'workout')}")

        score = 1.0 - (len(issues) * 0.1)
        score = max(0, score)

        return CriterionResult(
            criterion=EvaluationCriteria.STRUCTURE,
            passed=score >= 0.7,
            score=score,
            details=f"Structure check found {len(issues)} issues",
            issues=issues
        )

    def _evaluate_goal_alignment(
        self,
        plan: dict,
        assessment: dict
    ) -> CriterionResult:
        """Evaluate if plan aligns with stated goals."""
        issues = []
        goals = assessment.get("fitness_goals", {}).get("priority_focus", [])

        all_exercises = self._extract_all_exercises(plan)

        # Goal-specific exercise patterns
        goal_indicators = {
            "fat_loss": ["circuit", "superset", "conditioning", "cardio", "metabolic"],
            "strength": ["squat", "bench", "deadlift", "press", "row"],
            "muscle_gain": ["isolation", "hypertrophy", "curl", "extension"],
            "mobility": ["stretch", "mobility", "foam", "flexibility"],
            "endurance": ["cardio", "run", "bike", "row", "intervals"],
            "general_fitness": ["full body", "compound", "functional"]
        }

        for goal in goals:
            if goal in goal_indicators:
                indicators = goal_indicators[goal]
                found = any(
                    any(ind.lower() in ex.lower() for ind in indicators)
                    for ex in all_exercises
                )
                if not found:
                    # Check plan notes and focus
                    plan_text = json.dumps(plan).lower()
                    found = any(ind.lower() in plan_text for ind in indicators)

                if not found:
                    issues.append(f"Goal '{goal}' not clearly addressed in plan")

        score = 1.0 - (len(issues) * 0.25)
        score = max(0, score)

        return CriterionResult(
            criterion=EvaluationCriteria.GOAL_ALIGNMENT,
            passed=score >= 0.6,
            score=score,
            details=f"Goal alignment check found {len(issues)} issues",
            issues=issues
        )

    def _extract_all_exercises(self, plan: dict) -> list:
        """Extract all exercise names from plan."""
        exercises = []
        for day in plan.get("workout_days", []):
            for ex in day.get("exercises", []):
                name = ex.get("exercise_name", ex.get("name", ""))
                if name:
                    exercises.append(name)
        return exercises

    def _get_avg_rpe(self, days: list) -> float:
        """Calculate average RPE across workout days."""
        total_rpe = 0
        count = 0
        for day in days:
            for ex in day.get("exercises", []):
                rpe = ex.get("rpe", 7)
                total_rpe += rpe
                count += 1
        return total_rpe / count if count > 0 else 7

    def _generate_summary(
        self,
        overall_score: float,
        criterion_results: dict
    ) -> str:
        """Generate evaluation summary."""
        grade = "A" if overall_score >= 0.9 else "B" if overall_score >= 0.8 else "C" if overall_score >= 0.7 else "D" if overall_score >= 0.6 else "F"

        passed_criteria = sum(1 for r in criterion_results.values() if r.passed)
        total_criteria = len(criterion_results)

        return f"Grade: {grade} ({overall_score:.1%}) - Passed {passed_criteria}/{total_criteria} criteria"


async def run_evaluation_suite(
    agent,
    test_cases: list,
    verbose: bool = True
) -> dict:
    """
    Run evaluation suite against the agent.

    Args:
        agent: WorkoutPlanningAgent instance
        test_cases: List of test cases
        verbose: Print detailed output

    Returns:
        Summary of evaluation results
    """
    evaluator = PlanEvaluator()
    results = []

    for test_case in test_cases:
        if verbose:
            print(f"\n{'='*60}")
            print(f"Test Case: {test_case['name']}")
            print(f"{'='*60}")

        # Generate plan
        plan = await agent.generate_plan(
            assessment=test_case["assessment"],
            coach_preferences=test_case.get("coach_preferences", {})
        )

        # Evaluate
        result = evaluator.evaluate(plan, test_case)
        results.append(result)

        if verbose:
            print(f"\nResult: {result.summary}")
            if result.recommendations:
                print("Recommendations:")
                for rec in result.recommendations[:5]:
                    print(f"  - {rec}")

    # Summary
    passed = sum(1 for r in results if r.overall_passed)
    avg_score = sum(r.overall_score for r in results) / len(results) if results else 0

    summary = {
        "total_tests": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "average_score": avg_score,
        "results": [
            {
                "name": r.test_case_name,
                "passed": r.overall_passed,
                "score": r.overall_score,
                "summary": r.summary
            }
            for r in results
        ]
    }

    if verbose:
        print(f"\n{'='*60}")
        print("EVALUATION SUMMARY")
        print(f"{'='*60}")
        print(f"Passed: {passed}/{len(results)}")
        print(f"Average Score: {avg_score:.1%}")

    return summary
