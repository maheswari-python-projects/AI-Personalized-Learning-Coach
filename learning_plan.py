
import re
from ai_service import generate_ai_response


def generate_backup_plan(subject, goal, level, duration, daily_minutes):

    match = re.search(r"\d+", str(duration))
    duration = int(match.group()) if match else 7
    duration = max(1, min(duration, 30))

    match = re.search(r"\d+", str(daily_minutes))
    daily_minutes = int(match.group()) if match else 30
    daily_minutes = max(10, daily_minutes)

    topics = [
        "Introduction and Basic Concepts",
        "Important Fundamentals",
        "Core Concepts",
        "Practical Examples",
        "Problem Solving",
        "Advanced Concepts",
        "Revision and Practice"
    ]

    plan = f"""
# Personalized Study Plan

**Subject:** {subject}

**Goal:** {goal}

**Level:** {level}

**Duration:** {duration} days

**Daily Study Time:** {daily_minutes} minutes

Note: This is a backup study plan because the AI service
is temporarily unavailable.
"""

    for day in range(1, duration + 1):
        topic = topics[(day - 1) % len(topics)]

        plan += f"""

## Day {day}: {topic}

- **Topic:** {topic} in {subject}
- **Objective:** Understand the important concepts.
- **Study Time:** {daily_minutes} minutes
- **Practice Activity:** Read the topic, write important points,
  and solve 3 practice questions.
- **Revision:** Review the previous day's topic.
"""

    return plan


def generate_study_plan(subject, goal, level, duration, daily_minutes):

    prompt = f"""
    You are a personalized learning coach.

    Create a study plan using these student details:
    Subject: {subject}
    Learning goal: {goal}
    Current level: {level}
    Duration: {duration}
    Daily study time: {daily_minutes} minutes

    Requirements:
    1. Create a plan for each day.
    2. Include topic, objectives, estimated time and practice activity.
    3. Match the student's current level.
    4. Keep the plan realistic.
    5. Include revision.
    6. Return the plan in clear, simple English.
    """

    try:
        return generate_ai_response(prompt)

    except Exception:
        return generate_backup_plan(
            subject, goal, level, duration, daily_minutes
        )


