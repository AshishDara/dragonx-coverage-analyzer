import json


def build_prompt(parsed_report: dict, analysis: list) -> str:
    """
    Build a structured prompt for Gemini
    """

    return f"""
You are a senior SoC verification engineer.

IP CONTEXT:
- Design: DMA Controller
- Domain: AXI-based DMA engine

TASK:
You are given:
1. A parsed functional coverage report
2. An analysis of uncovered bins with detected patterns

Your goal:
- Suggest SPECIFIC, REALISTIC test scenarios to close coverage gaps
- Use engineering reasoning, not generic advice
- Base suggestions on what is already covered

IMPORTANT RULES:
- Output MUST be valid JSON
- Do NOT include any explanation outside JSON
- Follow the exact output format shown below

EXPECTED OUTPUT FORMAT:
{{
  "suggestions": [
    {{
      "target_bin": "covergroup.coverpoint.bin",
      "priority": "high | medium | low",
      "difficulty": "easy | medium | hard",
      "suggestion": "one paragraph test idea",
      "test_outline": ["step 1", "step 2", "step 3"],
      "dependencies": ["optional dependency"],
      "reasoning": "why this test will close the bin"
    }}
  ]
}}

PARSED COVERAGE REPORT:
{json.dumps(parsed_report, indent=2)}

COVERAGE ANALYSIS:
{json.dumps(analysis, indent=2)}
"""
