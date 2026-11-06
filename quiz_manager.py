

import json
from ai_service import generate_ai_response


def get_backup_quiz(subject, num_questions):
    if subject.strip().lower() == "python":
        questions = [
            {
                "question": "Which keyword is used to define a function in Python?",
                "options": ["function", "def", "fun", "define"],
                "answer": "def",
                "explanation": "The def keyword is used to define a function."
            },
            {
                "question": "Which data type is used to store True or False?",
                "options": ["int", "str", "bool", "float"],
                "answer": "bool",
                "explanation": "The bool data type stores True or False values."
            },
            {
                "question": "Which symbol is used for comments in Python?",
                "options": ["//", "#", "/*", "--"],
                "answer": "#",
                "explanation": "The # symbol is used for single-line comments."
            },
            {
                "question": "Which function displays output in Python?",
                "options": ["show()", "display()", "print()", "output()"],
                "answer": "print()",
                "explanation": "The print() function displays output."
            },
            {
                "question": "Which operator is used for exponentiation?",
                "options": ["*", "**", "//", "%"],
                "answer": "**",
                "explanation": "The ** operator performs exponentiation."
            }
        ]

        return questions[:num_questions]

    raise RuntimeError(
        "Gemini is temporarily unavailable. Please try again later."
    )


def generate_quiz(subject, level, num_questions=5):
    prompt = f"""
    Create {num_questions} multiple-choice quiz questions.

    Subject: {subject}
    Student level: {level}

    Return ONLY valid JSON in this format:
    {{
        "questions": [
            {{
                "question": "Question text",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "answer": "Option A",
                "explanation": "Explain why this is correct"
            }}
        ]
    }}

    Make sure every question has exactly four options.
    The answer must exactly match one of the options.
    """

    try:
        response = generate_ai_response(prompt)
        response = response.strip()

        if response.startswith("```"):
            response = response.split("\n", 1)[1]
            response = response.rsplit("```", 1)[0].strip()

        quiz_data = json.loads(response)
        questions = quiz_data["questions"]

        for question in questions:
            if len(question["options"]) != 4:
                raise ValueError("Each question must have four options.")

            if question["answer"] not in question["options"]:
                raise ValueError("Invalid correct answer.")

        return questions

    except Exception:
        return get_backup_quiz(subject, num_questions)
