from google import genai
import json
import time


GEMINI_API_KEY = "AIzaSyCYVqmdDSWbRrC5C7rWEfgBcoTgYF7PJEY"

# Minimum delay between LLM calls (seconds)
MIN_API_INTERVAL = 2.0


class GeminiClient:
    def __init__(self):
        try:
            self.client = genai.Client(api_key=GEMINI_API_KEY)
        except Exception as e:
            print("[LLM INIT ERROR]", str(e))
            self.client = None

        # Track last API call time
        self.last_call_time = 0.0

    def _rate_limit(self):
        """
        Enforce minimum interval between API calls
        """
        now = time.time()
        elapsed = now - self.last_call_time

        if elapsed < MIN_API_INTERVAL:
            sleep_time = MIN_API_INTERVAL - elapsed
            time.sleep(sleep_time)

        self.last_call_time = time.time()

    def generate_json(self, prompt: str) -> dict:
        """
        Safely call Gemini with rate limiting and error handling.
        Returns valid JSON or a safe fallback structure.
        """

        if not self.client:
            return {
                "suggestions": [],
                "error": "Gemini client not initialized"
            }

        try:
            # ---- Rate limiting ----
            self._rate_limit()

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            if not response or not response.text:
                raise ValueError("Empty response from Gemini")

            text = response.text.strip()

            # ---- JSON parsing ----
            try:
                return json.loads(text)
            except json.JSONDecodeError:
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
