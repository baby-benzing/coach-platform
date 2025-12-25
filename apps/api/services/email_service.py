import resend
from config import get_settings
from datetime import datetime


class EmailService:
    """Email service using Resend."""

    def __init__(self):
        settings = get_settings()
        resend.api_key = settings.resend_api_key
        self.from_email = settings.from_email

    async def send_workout_plan(
        self,
        coach_email: str,
        coach_name: str,
        client_email: str,
        client_name: str,
        plan_name: str,
        plan_data: dict,
    ) -> bool:
        """Send workout plan email to coach and client."""

        html_content = self._generate_plan_html(
            coach_name, client_name, plan_name, plan_data
        )

        try:
            # Send to both coach and client
            params = {
                "from": f"Coach Platform <{self.from_email}>",
                "to": [client_email, coach_email],
                "subject": f"Your Workout Plan: {plan_name}",
                "html": html_content,
            }

            resend.Emails.send(params)
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    def _generate_plan_html(
        self, coach_name: str, client_name: str, plan_name: str, plan_data: dict
    ) -> str:
        """Generate HTML email template for workout plan."""

        days_html = ""
        workout_days = plan_data.get("days", [])

        # Group by week
        weeks = {}
        for day in workout_days:
            week_num = day.get("week_number", 1)
            if week_num not in weeks:
                weeks[week_num] = []
            weeks[week_num].append(day)

        for week_num in sorted(weeks.keys()):
            days_html += f"""
            <div style="margin-bottom: 24px;">
                <h3 style="color: #0ea5e9; margin-bottom: 12px;">Week {week_num}</h3>
            """

            for day in weeks[week_num]:
                day_name = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"][
                    day.get("day_of_week", 0)
                ]
                exercises_html = ""

                for exercise in day.get("exercises", []):
                    if exercise.get("sets") and exercise.get("reps"):
                        detail = f"{exercise['sets']} x {exercise['reps']}"
                        if exercise.get("weight_kg"):
                            detail += f" @ {exercise['weight_kg']}kg"
                    elif exercise.get("duration_minutes"):
                        detail = f"{exercise['duration_minutes']} min"
                        if exercise.get("distance_km"):
                            detail += f" / {exercise['distance_km']}km"
                    else:
                        detail = ""

                    exercises_html += f"""
                    <div style="padding: 8px 0; border-bottom: 1px solid #e5e7eb;">
                        <strong>{exercise.get('exercise_name', 'Exercise')}</strong>
                        <span style="color: #6b7280; margin-left: 12px;">{detail}</span>
                    </div>
                    """

                days_html += f"""
                <div style="background: #f9fafb; border-radius: 8px; padding: 16px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <strong style="color: #111827;">{day_name} - {day.get('name', 'Workout')}</strong>
                        <span style="color: #6b7280; font-size: 14px;">{day.get('focus', '')}</span>
                    </div>
                    {exercises_html}
                    {f"<p style='color: #6b7280; font-size: 12px; margin-top: 8px;'>{day.get('notes', '')}</p>" if day.get('notes') else ''}
                </div>
                """

            days_html += "</div>"

        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #111827; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="text-align: center; margin-bottom: 32px;">
        <h1 style="color: #0ea5e9; margin-bottom: 8px;">Coach Platform</h1>
        <p style="color: #6b7280;">Your personalized workout plan is ready!</p>
    </div>

    <div style="background: linear-gradient(135deg, #0ea5e9, #d946ef); color: white; border-radius: 12px; padding: 24px; margin-bottom: 24px;">
        <h2 style="margin: 0 0 8px 0;">{plan_name}</h2>
        <p style="margin: 0; opacity: 0.9;">Prepared for {client_name} by Coach {coach_name}</p>
        <p style="margin: 8px 0 0 0; font-size: 14px; opacity: 0.8;">
            {plan_data.get('weeks', 4)} weeks • Starting {datetime.now().strftime('%B %d, %Y')}
        </p>
    </div>

    {days_html}

    {f"<div style='background: #fef3c7; border-radius: 8px; padding: 16px; margin-top: 24px;'><strong>Coach Notes:</strong><p style='margin: 8px 0 0 0;'>{plan_data.get('coach_notes', '')}</p></div>" if plan_data.get('coach_notes') else ''}

    <div style="text-align: center; margin-top: 32px; padding-top: 24px; border-top: 1px solid #e5e7eb; color: #6b7280; font-size: 14px;">
        <p>Questions? Reply to this email to contact your coach.</p>
        <p style="margin-top: 8px;">Powered by Coach Platform</p>
    </div>
</body>
</html>
"""
