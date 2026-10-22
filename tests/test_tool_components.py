"""Unit tests for LocalStorageManager."""

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


def test_tool_components(driver: Firefox) -> None:
    wait = WebDriverWait(driver, 10)

    run_button = driver.find_element(By.ID, "execution_test_run")
    wait.until(expected_conditions.element_to_be_clickable(run_button))
    run_button.click()

    # The progress bar should be visible and the output textareas should have content. The progress bar, the output
    # windows and the buttons each have their own binding, so they don't necessarily update in the same pass.
    progress_bar_running = driver.find_element(By.ID, "progress_bar_test_show_progress")
    outputs = driver.find_element(By.ID, "tool_outputs_test_outputs")
    errors = driver.find_element(By.ID, "tool_outputs_test_errors")
    wait.until(expected_conditions.visibility_of(progress_bar_running))
    wait.until(lambda _: outputs.get_attribute("value") == "test_output")
    wait.until(lambda _: errors.get_attribute("value") == "test_error")
    assert outputs.get_attribute("value") == "test_output"
    assert errors.get_attribute("value") == "test_error"

    # Cancel stays disabled until the running state reaches the buttons, which can lag the progress bar becoming
    # visible. Clicking it before then does nothing, and the test would then time out waiting for a cancel that
    # was never requested.
    cancel_button = driver.find_element(By.ID, "execution_test_cancel")
    wait.until(expected_conditions.element_to_be_clickable(cancel_button))
    cancel_button.click()
    # The finished bar should be visible.
    wait.until_not(expected_conditions.visibility_of(progress_bar_running))
    progress_bar_finished = driver.find_element(By.ID, "progress_bar_test_show_ok")
    wait.until(expected_conditions.visibility_of(progress_bar_finished))
