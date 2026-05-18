"""Unit tests for LocalStorageManager."""

from selenium.webdriver import ActionChains, Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


def test_tool_components(driver: Firefox) -> None:
    wait = WebDriverWait(driver, 5)

    run_button = driver.find_element(By.ID, "execution_test_run")
    cancel_button = driver.find_element(By.ID, "execution_test_cancel")
    progress_bar_running = driver.find_element(By.ID, "progress_bar_test_show_progress")
    progress_bar_finished = driver.find_element(By.ID, "progress_bar_test_show_ok")
    outputs = driver.find_element(By.ID, "tool_outputs_test_outputs")
    errors = driver.find_element(By.ID, "tool_outputs_test_errors")

    ActionChains(driver).click(run_button).perform()
    # The progress bar should be visible and the output textareas should have content.
    wait.until(expected_conditions.visibility_of(progress_bar_running))
    assert outputs.get_attribute("value") == "test_output"
    assert errors.get_attribute("value") == "test_error"

    ActionChains(driver).click(cancel_button).perform()
    # The finished bar should be visible.
    wait.until_not(expected_conditions.visibility_of(progress_bar_running))
    wait.until(expected_conditions.visibility_of(progress_bar_finished))
