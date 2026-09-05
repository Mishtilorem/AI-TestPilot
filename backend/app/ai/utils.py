import json
import re


def strip_code_fences(text: str) -> str:
    """Remove ```lang ... ``` fences if a model wrapped its output in them."""
    text = text.strip()
    match = re.match(r"^```[a-zA-Z]*\n(.*)\n```$", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text


def sanitize_selenium_script(code: str) -> str:
    """Drop driver lifecycle calls — the test runner owns creating/quitting the driver."""
    code = strip_code_fences(code)
    kept = [
        line
        for line in code.splitlines()
        if "driver.quit(" not in line and "driver.close(" not in line
    ]
    return "\n".join(kept).strip()


def parse_json(raw: str) -> dict:
    """Parse model JSON output, tolerating surrounding text or code fences."""
    cleaned = strip_code_fences(raw)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Fall back to the first {...} block in the string.
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(cleaned[start : end + 1])
        raise
