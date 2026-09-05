TEST_CASE_SYSTEM_PROMPT = (
    "You are a senior QA engineer. Generate clear, comprehensive test cases from a "
    "requirement. Respond with valid JSON only — no markdown, no commentary."
)


def build_test_case_prompt(requirement: str, target_url: str) -> str:
    return f"""Generate test cases for this requirement on the web app at {target_url}.

REQUIREMENT:
{requirement}

Return JSON with this exact shape:
{{
  "test_cases": [
    {{
      "title": "short title",
      "description": "step-by-step actions to perform",
      "expected_result": "what should happen",
      "category": "positive | negative | boundary | validation | security"
    }}
  ]
}}

Include at least: 2 positive, 2 negative, 1 boundary, 1 validation, and 1 security test case."""
