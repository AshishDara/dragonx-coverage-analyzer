from llm.gemini_client import GeminiClient
from llm.prompt_builder import build_prompt


def generate_test_suggestions(parsed_report: dict, analysis: list) -> dict:
    """
    Generate test suggestions using Gemini
    """
    client = GeminiClient()
    prompt = build_prompt(parsed_report, analysis)

    return client.generate_json(prompt)
