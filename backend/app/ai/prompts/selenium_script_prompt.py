SCRIPT_SYSTEM_PROMPT = (
    "You are a senior test automation engineer. Write a single, runnable Selenium "
    "Python script for one test case. Respond with raw Python code only — no markdown "
    "fences, no explanation."
)


def build_script_prompt(title: str, description: str, expected_result: str, target_url: str) -> str:
    return f"""Write a Selenium script in Python for this test case on {target_url}.

TEST CASE
Title: {title}
Steps: {description}
Expected result: {expected_result}

ENVIRONMENT (already provided — do not redefine):
- A WebDriver instance named `driver` is ALREADY in scope. Do NOT create or quit it.
- Start with: driver.get("{target_url}")

LOCATOR RULES (follow strictly to avoid invalid selectors):
- Prefer By.ID or By.CSS_SELECTOR. Use By.CSS_SELECTOR for anything with multiple
  classes — e.g. element with classes "flash error" => (By.CSS_SELECTOR, ".flash.error").
- NEVER use By.CLASS_NAME with a value containing a space (it is invalid).
- Use simple, conventional selectors (input#username, input#password,
  button[type='submit'], etc.).

WAIT / ASSERTION RULES:
- Use WebDriverWait + expected_conditions. Never use time.sleep.
- Import: from selenium.webdriver.common.by import By
- Make assertions resilient: assert that expected text is CONTAINED in the element/page
  (substring, case-insensitive where sensible), not an exact string match.
- If the test expects a successful login but no valid credentials are given in the steps,
  assert that the page changed (URL changed or a post-login element/text appeared) rather
  than guessing exact credentials.

OUTPUT:
- A single straight-line script (no functions, no `if __name__` block, no try/except).
- Raw Python only."""
