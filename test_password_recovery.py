import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.ui
def test_recovery_page_opens_from_login(driver, base_url):
    driver.get(base_url)

    wait = WebDriverWait(driver, 10)

    forgot_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Забыл пароль")))
    forgot_link.click()

    wait.until(EC.url_contains("reset-credentials"))

    title = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(., 'Восстановление пароля')]")))
    assert title is not None

    btn = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Продолжить')]")))
    assert btn.is_displayed()

@pytest.mark.ui
def test_recovery_page_has_all_tabs(driver, base_url):
    driver.get(base_url)

    wait = WebDriverWait(driver, 10)

    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Забыл пароль"))).click()
    wait.until(EC.url_contains("reset-credentials"))

    tabs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".rt-tab")))
    tab_texts = [t.text.strip() for t in tabs]

    assert "Телефон" in tab_texts
    assert "Почта" in tab_texts
    assert "Логин" in tab_texts
    assert "Лицевой счёт" in tab_texts
