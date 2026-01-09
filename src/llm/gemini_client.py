from google import genai
import json
import time



GEMINI_API_KEY = "AIzaSyCYVqmdDSWbRrC5C7rWEfgBcoTgYF7PJEY"


class GeminiClient:
    def __init__(self):
        try:
            self.client = genai.Client(api_key=GEMINI_API_KEY)
        except Exception as e:
            print("[LLM INIT ERROR]", str(e))
            self.client = None

    def generate_json(self, prompt: str) -> dict:
        """
        Safely call Gemini and return parsed JSON.
        On failure, return a safe fallback structure.
        """

        if not self.client:
            return {
                "suggestions": [],
                "error": "Gemini client not initialized"
            }

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            if not response or not response.text:
                raise ValueError("Empty response from Gemini")

            # Gemini sometimes returns extra text — extract JSON safely
            text = response.text.strip()

            # Try parsing directly
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                # Try to extract JSON block
                start = text.find("{")
                end = text.rfind("}")
                if start != -1 and end != -1:
                    return json.loads(text[start:end + 1])
                else:
                    raise ValueError("No valid JSON found in response")

        except Exception as e:
            print("[LLM ERROR]", str(e))
            return {
                "suggestions": [],
                "error": "LLM request failed, please retry later"
            }
