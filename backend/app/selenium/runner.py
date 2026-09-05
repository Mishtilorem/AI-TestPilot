import time
import os
import tempfile
import traceback
from app.core.config import settings
from app.selenium.drivers.driver_factory import create_chrome_driver
from app.selenium.utils.screenshot_utils import upload_screenshot
from app.models.test_result import ResultStatus


def execute_script(script_code: str, target_url: str, run_id: str, test_case_id: str) -> dict:
    """Run one AI-generated Selenium script and report the outcome.

    The script receives a ready `driver` in its namespace (it must not create or
    quit one). A clean finish = passed; any exception = failed, and we grab a
    screenshot of the final state for debugging.
    """
    driver = None
    started = time.perf_counter()
    status = ResultStatus.PASSED
    logs = ""
    screenshot_url = None

    try:
        # Creating the driver can fail if no Chrome is installed (e.g. a host
        # without a browser). Keep it inside try so that becomes a clean result,
        # not a crashed request.
        driver = create_chrome_driver(headless=settings.SELENIUM_HEADLESS)
        # The generated script brings its own imports; we just hand it the driver.
        exec(script_code, {"driver": driver})
        logs = "Test passed."
    except Exception:
        status = ResultStatus.FAILED
        logs = traceback.format_exc()
        if driver is not None:
            screenshot_url = _capture_screenshot(driver, run_id, test_case_id)
    finally:
        duration = round(time.perf_counter() - started, 2)
        if driver is not None:
            driver.quit()

    return {
        "status": status,
        "duration_seconds": duration,
        "logs": logs,
        "screenshot_url": screenshot_url,
    }


def _capture_screenshot(driver, run_id: str, test_case_id: str) -> str | None:
    try:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            path = f.name
        driver.save_screenshot(path)
        url = upload_screenshot(path, f"runs/{run_id}/{test_case_id}")
        os.unlink(path)
        return url
    except Exception:
        return None
