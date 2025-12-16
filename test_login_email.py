import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def go_to_email_tab(driver, base_url):
    driver.get(base_url)

    mail_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class,'rt-tab') and normalize-space()='Почта']")
        )
    )
    mail_tab.click()


@pytest.mark.ui
def test_login_email_success(driver, base_url, test_email, test_password):
    go_to_email_tab(driver, base_url)

    email_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    email_input.send_keys(test_email)
    password_input.send_keys(test_password)

    print("\n 20 секунд на ввод капчи\n")
    time.sleep(20)

    submit_btn.click()

    assert "login" not in driver.current_url.lower()


@pytest.mark.ui
def test_login_email_wrong_password(driver, base_url, test_email):
    go_to_email_tab(driver, base_url)

    email_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    email_input.send_keys(test_email)
    password_input.send_keys("Asdadasdd21331")

    print("\n 20 секунд на ввод капчи\n")
    time.sleep(20)

    submit_btn.click()

    error = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "form-error-message"))
    )
    assert "неверн" in error.text.lower()


@pytest.mark.ui
def test_login_email_empty_fields(driver, base_url):
    go_to_email_tab(driver, base_url)

    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_btn.click()

    errors = driver.find_elements(By.CSS_SELECTOR, ".rt-input-container__meta--error")
    assert len(errors) >= 1


@pytest.mark.ui
def test_login_email_invalid_format_no_at(driver, base_url):
    go_to_email_tab(driver, base_url)

    email_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    email_input.send_keys("testikmail.ru")
    password_input.send_keys("Asdsasda131")

    print("\n 20 секунд на ввод капчи\n")
    time.sleep(20)

    submit_btn.click()

    error = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "form-error-message"))
    )
    assert "неверн" in error.text.lower() or "логин" in error.text.lower()


@pytest.mark.ui
def test_login_email_invalid_format_no_domain(driver, base_url):
    go_to_email_tab(driver, base_url)

    email_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    email_input.send_keys("testik@")
    password_input.send_keys("Asdads134")

    print("\n 20 секунд на ввод капчи\n")
    time.sleep(20)

    submit_btn.click()

    error = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "form-error-message"))
    )
    assert "неверн" in error.text.lower() or "логин" in error.text.lower()


@pytest.mark.ui
def test_login_email_wrong_email_correct_password(driver, base_url, test_password):
    go_to_email_tab(driver, base_url)

    email_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    email_input.send_keys("testik@mail.ru")
    password_input.send_keys(test_password)

    print("\n 20 секунд на ввод капчи\n")
    time.sleep(20)

    submit_btn.click()

    error = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "form-error-message"))
    )
    assert "неверн" in error.text.lower() or "логин" in error.text.lower()


@pytest.mark.ui
def test_login_email_case_sensitive_password(driver, base_url, test_email, test_password):
    go_to_email_tab(driver, base_url)

    email_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    email_input.send_keys(test_email)
    password_input.send_keys(test_password.lower())

    print("\n 20 секунд на ввод капчи\n")
    time.sleep(20)

    submit_btn.click()

    error = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "form-error-message"))
    )
    assert "неверн" in error.text.lower() or "пароль" in error.text.lower()


@pytest.mark.ui
def test_login_email_whitespace_trim(driver, base_url, test_email, test_password):
    go_to_email_tab(driver, base_url)

    email_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    email_input.send_keys(f"  {test_email}  ")
    password_input.send_keys(test_password)

    print("\n 20 секунд на ввод капчи\n")
    time.sleep(20)

    submit_btn.click()

    assert "login" not in driver.current_url.lower()


@pytest.mark.ui
def test_login_email_password_mask(driver, base_url):
    go_to_email_tab(driver, base_url)

    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys("asdasdad")

    input_type = password_input.get_attribute("type")
    assert input_type == "password"


@pytest.mark.ui
def test_login_email_show_password_toggle(driver, base_url):
    go_to_email_tab(driver, base_url)

    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys("asdasdad")

    toggle = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "svg.rt-input__eye")
        )
    )
    toggle.click()

    input_type = password_input.get_attribute("type")
    assert input_type == "text"
