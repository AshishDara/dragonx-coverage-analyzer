
from google import genai
import json
import time
import hashlib
import os


GEMINI_API_KEY = "Paste your api key here"

# Rate limiting: minimum delay between API calls (seconds)
MIN_API_INTERVAL = 2.0

# Cache directory
CACHE_DIR = ".cache"


class GeminiClient:
    def __init__(self):
        try:
            self.client = genai.Client(api_key=GEMINI_API_KEY)
        except Exception as e:
            print("[LLM INIT ERROR]", str(e))
            self.client = None

        self.last_call_time = 0.0

        # Ensure cache directory exists
        os.makedirs(CACHE_DIR, exist_ok=True)

    def _rate_limit(self):
        now = time.time()
        elapsed = now - self.last_call_time
        if elapsed < MIN_API_INTERVAL:
            time.sleep(MIN_API_INTERVAL - elapsed)
        self.last_call_time = time.time()

    def _cache_path(self, prompt: str) -> str:
        """
        Compute cache file path based on prompt hash
        """
        prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
        return os.path.join(CACHE_DIR, f"{prompt_hash}.json")

    def generate_json(self, prompt: str) -> dict:
        """
        Safely call Gemini with:
        - caching
        - rate limiting
        - graceful error handling
        """

        cache_file = self._cache_path(prompt)

        # ---- Cache hit ----
        if os.path.exists(cache_file):
            try:
                with open(cache_file, "r") as f:
                    print("[CACHE HIT]")
                    return json.load(f)
            except Exception:
                # Corrupt cache → ignore and regenerate
                pass

        # ---- No client ----
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

            # ---- Parse JSON ----
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                start = text.find("{")
                end = text.rfind("}")
                if start != -1 and end != -1:
                    parsed = json.loads(text[start:end + 1])
                else:
                    raise ValueError("No valid JSON found in response")

            # ---- Save to cache ----
            with open(cache_file, "w") as f:
                json.dump(parsed, f, indent=2)

            return parsed

        except Exception as e:
            print("[LLM ERROR]", str(e))
            return {
                "suggestions": [],
                "error": "LLM request failed, please retry later"
            }
