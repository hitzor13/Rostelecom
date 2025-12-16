import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from test_login_email import go_to_email_tab


def login_via_email(driver, base_url, email, password):
    go_to_email_tab(driver, base_url)

    email_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    email_input.send_keys(email)
    password_input.send_keys(password)

    print("\n⚠️ 20 секунд на ввод капчи\n")
    time.sleep(20)

    submit_btn.click()


def logout(driver):
    logout_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "logout-btn"))
    )
    logout_btn.click()


@pytest.mark.ui
def test_logout(driver, base_url, test_email, test_password):
    login_via_email(driver, base_url, test_email, test_password)
    logout(driver)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )

    assert "login" in driver.current_url.lower() or "auth" in driver.current_url.lower()


@pytest.mark.ui
def test_relogin_after_logout(driver, base_url, test_email, test_password):
    login_via_email(driver, base_url, test_email, test_password)

    logout(driver)

    print("\n⚠️ 20 секунд на ввод капчи\n")
    time.sleep(20)

    login_via_email(driver, base_url, test_email, test_password)

    assert "login" not in driver.current_url.lower()
