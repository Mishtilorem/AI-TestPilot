ANALYSIS_SYSTEM_PROMPT = (
    "You are a senior test automation engineer doing root-cause analysis on a failed "
    "Selenium test. Be concise and practical. Respond with valid JSON only."
)


def build_analysis_prompt(test_title: str, script: str, logs: str) -> str:
    return f"""A Selenium test failed. Analyse why.

TEST CASE: {test_title}

SCRIPT:
{script}

FAILURE LOGS / TRACEBACK:
{logs}

Return JSON with this exact shape:
{{
  "root_cause": "the single most likely cause, one sentence",
  "explanation": "a short paragraph explaining what went wrong",
  "possible_fixes": ["concrete fix 1", "concrete fix 2"],
  "confidence": 0.0
}}

confidence is your confidence in the root cause, between 0.0 and 1.0."""
