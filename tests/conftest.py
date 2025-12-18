"""
Общие фикстуры для всех тестов
"""

import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from typing import Generator


@pytest.fixture(scope="function")
@allure.title("Инициализация WebDriver")
def driver() -> Generator[webdriver.Chrome, None, None]:
    """
    Фикстура для создания экземпляра WebDriver.

    Returns:
        Generator[webdriver.Chrome]: Экземпляр драйвера
    """
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    service = ChromeService(ChromeDriverManager().install())
    driver_instance = webdriver.Chrome(service=service, options=chrome_options)
    driver_instance.maximize_window()

    yield driver_instance

    driver_instance.quit()


@pytest.fixture(scope="function")
@allure.title("Подготовка API клиента")
def api_client() -> dict:
    """
    Фикстура для подготовки данных API клиента.

    Returns:
        dict: Конфигурация для API запросов
    """
    from config.credentials import API_KEY
    from config.settings import API_BASE_URL, GRAPHQL_URL

    return {
        "api_key": API_KEY,
        "base_url": API_BASE_URL,
        "graphql_url": GRAPHQL_URL,
        "headers": {
            "accept": "application/json",
            "X-API-KEY": API_KEY
        }
    }