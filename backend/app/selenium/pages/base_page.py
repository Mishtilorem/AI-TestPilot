from selenium.webdriver.remote.webdriver import WebDriver
from app.selenium.utils.wait_utils import wait_for_visible, wait_for_clickable


class BasePage:
    """Page Object Model base. Concrete pages subclass this and define their locators.

    Centralises the common interactions (navigate, type, click, read text) so that
    page classes stay small and tests read clearly.
    """

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def open(self, url: str) -> None:
        self.driver.get(url)

    def type(self, locator: tuple[str, str], text: str) -> None:
        element = wait_for_visible(self.driver, locator)
        element.clear()
        element.send_keys(text)

    def click(self, locator: tuple[str, str]) -> None:
        wait_for_clickable(self.driver, locator).click()

    def text_of(self, locator: tuple[str, str]) -> str:
        return wait_for_visible(self.driver, locator).text

    def is_visible(self, locator: tuple[str, str]) -> bool:
        try:
            wait_for_visible(self.driver, locator)
            return True
        except Exception:
            return False

    def current_url(self) -> str:
        return self.driver.current_url

    def title(self) -> str:
        return self.driver.title
