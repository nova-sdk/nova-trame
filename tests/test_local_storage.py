"""Unit tests for LocalStorageManager."""

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


def click_when_ready(driver: Firefox, selector: str) -> None:
    button = WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, selector)))
    # Click via JS so that the app bar and footer can't intercept the click if the button is scrolled under them.
    driver.execute_script("arguments[0].click();", button)


def test_local_storage(driver: Firefox) -> None:
    assert driver.execute_script("window.localStorage.getItem('local_storage_test');") is None

    text_field = WebDriverWait(driver, 10).until(
        expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "#local-storage-input"))
    )
    text_field.send_keys("1")

    click_when_ready(driver, "#local-storage-set")
    WebDriverWait(driver, 10).until(
        lambda *args: driver.execute_script("return window.localStorage.getItem('local_storage_test');") == "1"
    )

    click_when_ready(driver, "#local-storage-remove")
    assert driver.execute_script("window.localStorage.getItem('local_storage_test');") is None
