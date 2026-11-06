
import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


def generate_ai_response(prompt):
    if not api_key:
        raise ValueError("Gemini API key is missing.")

    client = genai.Client(api_key=api_key)

    for attempt in range(2):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            result = response.text

            if result is None or not result.strip():
                raise ValueError("AI returned an empty response.")

            return result.strip()

        except Exception:
            if attempt == 1:
                raise

            time.sleep(2)

    raise RuntimeError("AI response could not be generated.")
