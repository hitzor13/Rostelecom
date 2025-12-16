import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.ui
def test_tabs_presence(driver, base_url):
    driver.get(base_url)

    wait = WebDriverWait(driver, 10)

    tabs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".rt-tab")))
    texts = [t.text for t in tabs]

    assert "Телефон" in texts
    assert "Почта" in texts
    assert "Логин" in texts
    assert "Лицевой счёт" in texts


@pytest.mark.ui
def test_default_tab_is_phone(driver, base_url):
    driver.get(base_url)

    wait = WebDriverWait(driver, 10)
    active_tab = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".rt-tab.rt-tab--active")))

    assert "Телефон" in active_tab.text


@pytest.mark.ui
def test_auto_switch_to_email_tab(driver, base_url):
    driver.get(base_url)

    wait = WebDriverWait(driver, 10)

    username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
    username_input.click() # не переключает даже с таймслипом и кликом
    username_input.send_keys("k2kta@comfythings.com")
    username_input.click()

    time.sleep(3) # не переключает даже с таймслипом и кликом

    active_tab = driver.find_element(By.CSS_SELECTOR, ".rt-tab.rt-tab--active")

    assert "Почта" in active_tab.text


@pytest.mark.ui
def test_forgot_password_link_navigation(driver, base_url):
    driver.get(base_url)

    wait = WebDriverWait(driver, 10)

    forgot_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Забыл пароль")))
    forgot_link.click()

    assert "reset" in driver.current_url.lower() or "credentials" in driver.current_url.lower()


@pytest.mark.ui
def test_auto_switch_to_phone_tab(driver, base_url):
    driver.get(base_url)

    wait = WebDriverWait(driver, 10)

    phone_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
    phone_input.send_keys("89990001122")

    active_tab = driver.find_element(By.CSS_SELECTOR, ".rt-tab.rt-tab--active")

    assert "Телефон" in active_tab.text


@pytest.mark.ui
def test_forgot_password_link_color_default(driver, base_url):
    driver.get(base_url)

    wait = WebDriverWait(driver, 10)

    forgot_link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Забыл пароль")))
    color = forgot_link.value_of_css_property("color")

    assert color is not None and color != ""
