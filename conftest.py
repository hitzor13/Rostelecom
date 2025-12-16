import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="session")
def base_url():
    return "https://b2c.passport.rt.ru"


@pytest.fixture(scope="session")
def test_email():
    return os.getenv("TEST_RT_EMAIL", "k2kta@comfythings.com")


@pytest.fixture(scope="session")
def test_password():
    return os.getenv("TEST_RT_PASSWORD", "Qa321478965")


@pytest.fixture(scope="function")
def driver():
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)

    driver.delete_all_cookies()

    yield driver

    driver.delete_all_cookies()
    driver.quit()
