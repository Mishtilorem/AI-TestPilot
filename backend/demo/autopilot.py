"""
AI TestPilot — demo auto-pilot.

Drives the frontend UI in a visible browser so you can screen-record a hands-free
end-to-end demo: register -> create projects -> generate test cases -> generate
scripts -> run in a real browser -> AI failure analysis.

Usage (frontend on :3100, backend on :8000 must be running):
    cd backend && source venv/bin/activate
    python demo/autopilot.py

Env knobs:
    DEMO_BASE_URL          frontend URL (default http://localhost:3100)
    DEMO_HEADLESS=1        run the auto-pilot browser headless (for testing)
    DEMO_PACE=1.5          seconds to pause between actions (raise for slower video)
    SCRIPTS_PER_PROJECT=3  how many test cases to generate scripts for, per project
    DEMO_PROJECTS_LIMIT=3  how many projects to run
"""
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE = os.getenv("DEMO_BASE_URL", "http://localhost:3100")
HEADLESS = os.getenv("DEMO_HEADLESS") == "1"
PACE = float(os.getenv("DEMO_PACE", "1.5"))
SCRIPTS_PER_PROJECT = int(os.getenv("SCRIPTS_PER_PROJECT", "3"))
PROJECTS_LIMIT = int(os.getenv("DEMO_PROJECTS_LIMIT", "3"))

PROJECTS = [
    {
        "name": "Example Domain",
        "url": "https://example.com",
        "req": 'The homepage should load and display the heading "Example Domain".',
    },
    {
        "name": "The Internet Login",
        "url": "https://the-internet.herokuapp.com/login",
        "req": "User should be able to log in with a valid username and password and reach the secure area.",
    },
    {
        "name": "Sauce Demo",
        "url": "https://www.saucedemo.com/",
        "req": "User logs in with a username and password and lands on the products page.",
    },
]


def log(msg):
    print(f"[autopilot] {msg}", flush=True)


def pace(mult=1.0):
    time.sleep(PACE * mult)


def make_driver():
    opts = Options()
    if HEADLESS:
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1500,950")
    opts.add_argument("--disable-gpu")
    d = webdriver.Chrome(options=opts)
    if not HEADLESS:
        try:
            d.maximize_window()
        except Exception:
            pass
    return d


def wait(d, cond, t=30):
    return WebDriverWait(d, t).until(cond)


def click_text(d, tag, text, t=30):
    el = wait(d, EC.element_to_be_clickable((By.XPATH, f'//{tag}[contains(normalize-space(.), "{text}")]')), t)
    d.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
    pace(0.5)
    el.click()
    return el


def text_present(d, text):
    return bool(d.find_elements(By.XPATH, f'//*[contains(normalize-space(.), "{text}")]'))


def wait_text_gone(d, text, t=120):
    WebDriverWait(d, t).until_not(
        EC.presence_of_element_located((By.XPATH, f'//button[contains(normalize-space(.), "{text}")]'))
    )


def register(d):
    log("Registering a fresh account…")
    d.get(f"{BASE}/register")
    ts = int(time.time())
    email = f"demo_{ts}@testpilot.com"
    wait(d, EC.presence_of_element_located((By.ID, "name")))
    d.find_element(By.ID, "name").send_keys("Demo User")
    d.find_element(By.ID, "email").send_keys(email)
    d.find_element(By.ID, "password").send_keys("password123")
    pace()
    click_text(d, "button", "Create account")
    wait(d, EC.url_contains("/dashboard"), 30)
    log(f"Logged in as {email}")
    pace(2)


def create_and_open_project(d, p):
    log(f"Creating project: {p['name']}  ({p['url']})")
    d.get(f"{BASE}/projects")
    pace()
    click_text(d, "button", "New Project")
    wait(d, EC.presence_of_element_located((By.ID, "name")))
    d.find_element(By.ID, "name").send_keys(p["name"])
    d.find_element(By.ID, "target_url").send_keys(p["url"])
    pace()
    click_text(d, "button", "Create")
    # wait for the new project card to appear, then open it
    link = wait(
        d,
        EC.element_to_be_clickable((By.XPATH, f'//a[contains(@href, "/projects/")][.//*[contains(normalize-space(.), "{p["name"]}")]]')),
        30,
    )
    pace()
    link.click()
    wait(d, EC.presence_of_element_located((By.XPATH, '//button[contains(., "Requirements")]')))
    pace(1.5)


def add_requirement(d, req):
    log("Adding requirement…")
    inp = wait(d, EC.presence_of_element_located((By.CSS_SELECTOR, "input")))
    inp.click()
    inp.send_keys(req)
    pace()
    click_text(d, "button", "Add")
    pace(1.5)


def generate_test_cases(d):
    log("Generating test cases with AI…")
    click_text(d, "button", "Generate Test Cases")
    wait_text_gone(d, "Generating...", 120)  # button reverts when done
    log("Test cases generated.")
    pace(1.5)


def generate_scripts(d, n):
    log(f"Switching to Test Cases tab; generating up to {n} scripts…")
    click_text(d, "button", "Test Cases")
    wait(d, EC.presence_of_element_located((By.XPATH, "//table")))
    pace()
    for i in range(n):
        before = len(d.find_elements(By.XPATH, '//button[contains(normalize-space(.), "View")]'))
        gen_buttons = d.find_elements(By.XPATH, '//button[contains(normalize-space(.), "Generate Script")]')
        if not gen_buttons:
            break
        d.execute_script("arguments[0].scrollIntoView({block:'center'});", gen_buttons[0])
        pace(0.5)
        gen_buttons[0].click()
        # wait until a new "View" button shows up (script ready)
        try:
            WebDriverWait(d, 60).until(
                lambda drv: len(drv.find_elements(By.XPATH, '//button[contains(normalize-space(.), "View")]')) > before
            )
            log(f"  script {i + 1} ready")
        except Exception:
            log(f"  script {i + 1} timed out (continuing)")
        pace()


def run_tests(d):
    log("Running tests in a real browser…")
    click_text(d, "button", "Runs")
    pace()
    click_text(d, "button", "Run Tests")
    wait(d, EC.url_contains("/runs/"), 180)  # redirects to run detail when done
    log("Run complete — on run detail page.")
    pace(2)


def analyze_one_failure(d):
    analyze_buttons = d.find_elements(By.XPATH, '//button[contains(normalize-space(.), "Analyze")]')
    if not analyze_buttons:
        log("No failed tests to analyze (all passed).")
        return
    log("Analyzing a failed test with AI…")
    d.execute_script("arguments[0].scrollIntoView({block:'center'});", analyze_buttons[0])
    pace(0.5)
    analyze_buttons[0].click()
    try:
        ai_btn = WebDriverWait(d, 90).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(normalize-space(.), "AI Analysis")]'))
        )
        pace()
        ai_btn.click()  # open the analysis dialog
        wait(d, EC.presence_of_element_located((By.XPATH, '//*[contains(., "Root Cause")]')), 15)
        log("AI analysis shown.")
        pace(4)
        d.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)  # close dialog
    except Exception:
        log("Analysis step skipped (timeout).")
    pace()


def main():
    d = make_driver()
    try:
        register(d)
        for p in PROJECTS[:PROJECTS_LIMIT]:
            create_and_open_project(d, p)
            add_requirement(d, p["req"])
            generate_test_cases(d)
            generate_scripts(d, SCRIPTS_PER_PROJECT)
            run_tests(d)
            analyze_one_failure(d)
            log(f"Finished project: {p['name']}\n")
            pace(2)
        # end on the dashboard for a clean closing shot
        d.get(f"{BASE}/dashboard")
        pace(4)
        log("DEMO COMPLETE.")
    finally:
        if not HEADLESS:
            time.sleep(3)
        d.quit()


if __name__ == "__main__":
    sys.exit(main())
