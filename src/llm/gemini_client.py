from google import genai
import json



GEMINI_API_KEY = "AIzaSyCYVqmdDSWbRrC5C7rWEfgBcoTgYF7PJEY"


class GeminiClient:
    def __init__(self):
        # Initialize client with API key
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def generate_json(self, prompt: str) -> dict:
        """
        Send prompt to Gemini and return parsed JSON response
        """
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        # Gemini may wrap JSON in markdown
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            raise ValueError(
                "Gemini response is not valid JSON.\nRaw response:\n" + text
            )
