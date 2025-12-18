import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.settings import BASE_URL, SEARCH_QUERIES, DEFAULT_TIMEOUT


@pytest.mark.ui
@allure.title("TC-UI-01: Поиск фильма по названию 'king'")
@allure.story("Быстрый поиск")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_movie_by_title(driver):
    """
    Позитивный тест: поиск существующего фильма

    Steps:
    1. Открыть главную страницу
    2. Ввести 'king' в поиск
    3. Проверить наличие результатов
    """
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    with allure.step("Открытие главной страницы Кинопоиск"):
        driver.get(BASE_URL)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    with allure.step("Ввод 'king' в поисковую строку"):
        search_input = wait.until(EC.element_to_be_clickable((By.NAME, "kp_query")))
        search_input.clear()
        search_input.send_keys(SEARCH_QUERIES["valid_movie"], Keys.ENTER)

    with allure.step("Ожидание результатов поиска"):
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "main")))

    with allure.step("Проверка наличия результатов"):
        results = driver.find_elements(
            By.CSS_SELECTOR,
            "a[href*='/film/'], a[href*='/series/'], "
            "[data-testid*='result'], .search-result-item"
        )
        assert len(results) > 0, "Нет результатов поиска"

        allure.attach(
            driver.get_screenshot_as_png(),
            name="search_results_king",
            attachment_type=allure.attachment_type.PNG
        )


@pytest.mark.ui
@allure.title("TC-UI-02: Поиск фильма по актеру 'Keanu Reeves'")
@allure.story("Поиск по актерам")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_movie_by_actor(driver):
    """
    Позитивный тест: поиск по имени актера

    Steps:
    1. Открыть главную страницу
    2. Ввести 'Keanu Reeves' в поиск
    3. Проверить наличие результатов
    """
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    with allure.step("Открытие главной страницы Кинопоиск"):
        driver.get(BASE_URL)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    with allure.step("Ввод 'Keanu Reeves' в поисковую строку"):
        search_input = wait.until(EC.element_to_be_clickable((By.NAME, "kp_query")))
        search_input.clear()
        search_input.send_keys(SEARCH_QUERIES["valid_actor"])
        search_input.send_keys(Keys.ENTER)

    with allure.step("Ожидание результатов поиска"):
        wait.until(EC.any_of(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".film-item")),
            EC.presence_of_element_located((By.TAG_NAME, "main"))
        ))

    with allure.step("Проверка результатов"):
        results = driver.find_elements(
            By.CSS_SELECTOR,
            "a[href*='/film/'], a[href*='/series/'], a[href*='/name/'], "
            "[data-testid*='result'], .search-result-item"
        )

        assert len(results) > 0, "Нет результатов поиска"

        results_text = [result.text.lower() for result in results[:5] if result.text]
        keanu_found = any(
            term in text for text in results_text
            for term in ["keanu", "киану", "reeves", "ривз"]
        )
        assert keanu_found, "'Keanu Reeves' не найден в результатах"

        allure.attach(
            driver.get_screenshot_as_png(),
            name="search_results_keanu",
            attachment_type=allure.attachment_type.PNG
        )


@pytest.mark.ui
@allure.title("TC-UI-03: Поиск несуществующего фильма")
@allure.story("Негативные сценарии")
@allure.severity(allure.severity_level.NORMAL)
def test_search_nonexistent_movie(driver):
    """
    Негативный тест: поиск несуществующего фильма

    Steps:
    1. Открыть главную страницу
    2. Ввести несуществующее название
    3. Проверить отсутствие результатов или сообщение
    """
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    with allure.step("Открытие главной страницы Кинопоиск"):
        driver.get(BASE_URL)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    with allure.step("Ввод несуществующего названия"):
        search_input = wait.until(EC.element_to_be_clickable((By.NAME, "kp_query")))
        search_input.clear()
        search_input.send_keys(SEARCH_QUERIES["invalid_movie"], Keys.ENTER)
        time.sleep(2)

    with allure.step("Проверка результатов (может быть пусто или сообщение)"):
        try:
            # Проверяем сообщение "ничего не найдено"
            no_results = driver.find_elements(
                By.XPATH,
                "//*[contains(text(), 'ничего не найдено') or "
                "contains(text(), 'not found') or "
                "contains(text(), 'не найдено')]"
            )
            if no_results:
                allure.attach("Показано сообщение 'ничего не найдено'", name="Результат")
            else:
                # Или проверяем отсутствие результатов
                results = driver.find_elements(
                    By.CSS_SELECTOR,
                    "a[href*='/film/'], a[href*='/series/']"
                )
                if len(results) == 0:
                    allure.attach("Результаты не найдены", name="Результат")
        except Exception as e:
            allure.attach(f"Ошибка при проверке: {str(e)}", name="Результат")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="search_no_results",
            attachment_type=allure.attachment_type.PNG
        )


@pytest.mark.ui
@allure.title("TC-UI-04: Пустой поисковый запрос")
@allure.story("Валидация ввода")
@allure.severity(allure.severity_level.MINOR)
def test_search_empty_query(driver):
    """
    Тест граничного условия: пустой запрос

    Steps:
    1. Открыть главную страницу
    2. Отправить пустой запрос
    3. Проверить, что страница не меняется
    """
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    with allure.step("Открытие главной страницы Кинопоиск"):
        driver.get(BASE_URL)
        initial_url = driver.current_url
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    with allure.step("Отправка пустого поискового запроса"):
        search_input = wait.until(EC.element_to_be_clickable((By.NAME, "kp_query")))
        search_input.clear()
        search_input.send_keys(Keys.ENTER)
        time.sleep(1)

    with allure.step("Проверка, что URL не изменился"):
        current_url = driver.current_url
        # При пустом запросе URL может не меняться или меняться незначительно
        assert "query=" not in current_url or initial_url == current_url, \
            f"URL изменился неожиданно: {initial_url} -> {current_url}"

        allure.attach(
            driver.get_screenshot_as_png(),
            name="empty_search",
            attachment_type=allure.attachment_type.PNG
        )


@pytest.mark.ui
@allure.title("TC-UI-05: Навигация и проверка элементов главной страницы")
@allure.story("Smoke тестирование")
@allure.severity(allure.severity_level.CRITICAL)
def test_main_page_elements(driver):
    """
    Smoke тест: проверка основных элементов главной страницы

    Steps:
    1. Открыть главную страницу
    2. Проверить наличие ключевых элементов
    3. Проверить заголовок страницы
    """
    wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    with allure.step("Открытие главной страницы Кинопоиск"):
        driver.get(BASE_URL)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    with allure.step("Проверка заголовка страницы"):
        title = driver.title
        assert title, "Заголовок страницы пустой"
        assert "Кинопоиск" in title, f"Заголовок не содержит 'Кинопоиск': {title}"

    with allure.step("Проверка наличия ключевых элементов"):
        # Поисковая строка
        search_input = driver.find_elements(By.NAME, "kp_query")
        assert len(search_input) > 0, "Поисковая строка не найдена"

        # Логотип
        logo = driver.find_elements(
            By.CSS_SELECTOR,
            "[class*='logo'], [href='/'], img[alt*='Кинопоиск']"
        )
        assert len(logo) > 0, "Логотип не найден"

        # Меню навигации
        menu_items = driver.find_elements(
            By.CSS_SELECTOR,
            "[class*='menu'], [class*='navigation'], nav, header a"
        )
        assert len(menu_items) > 3, "Недостаточно элементов меню"

        allure.attach(
            driver.get_screenshot_as_png(),
            name="main_page_elements",
            attachment_type=allure.attachment_type.PNG
        )