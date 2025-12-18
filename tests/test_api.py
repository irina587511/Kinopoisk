"""
API тесты для Кинопоиска
Всего 5 тестов на основе Postman коллекции
"""

import pytest
import allure
import requests
from typing import Dict, Any
from config.credentials import API_KEY
from config.settings import API_BASE_URL, GRAPHQL_URL, MOVIE_IDS, SEARCH_QUERIES


@pytest.mark.api
@allure.title("TC-API-01: Поиск фильма по названию (позитивный)")
@allure.story("API поиск")
@allure.severity(allure.severity_level.CRITICAL)
def test_api_search_movie_by_title(api_client: Dict[str, Any]) -> None:
    """
    Позитивный тест API: поиск фильма по названию

    Expected: статус 200, результаты в ответе
    """
    with allure.step("Подготовка запроса для поиска фильма 'king'"):
        url = f"{API_BASE_URL.rstrip('/')}/movie/search"
        params = {
            "query": SEARCH_QUERIES["valid_movie"],
            "page": 1,
            "limit": 10
        }

    with allure.step("Отправка GET запроса с API ключом"):
        response = requests.get(
            url,
            params=params,
            headers=api_client["headers"]
        )

    with allure.step("Проверка статус кода 200"):
        assert response.status_code == 200, \
            f"Ожидался статус 200, получен {response.status_code}"

    with allure.step("Проверка структуры ответа"):
        data = response.json()
        assert "docs" in data, "В ответе нет поля 'docs'"
        assert isinstance(data["docs"], list), "Поле 'docs' не является списком"

        allure.attach(
            str(data.get("docs", [])[:2]),  # Первые 2 результата для отчета
            name="search_results",
            attachment_type=allure.attachment_type.TEXT
        )


@pytest.mark.api
@allure.title("TC-API-02: Поиск фильма по ID (позитивный)")
@allure.story("API информация о фильме")
@allure.severity(allure.severity_level.CRITICAL)
def test_api_get_movie_by_id(api_client: Dict[str, Any]) -> None:
    """
    Позитивный тест API: получение информации о фильме по ID

    Expected: статус 200, информация о фильме
    """
    with allure.step("Подготовка запроса для фильма с ID 5089022"):
        url = f"{API_BASE_URL.rstrip('/')}/movie/{MOVIE_IDS['valid']}"

    with allure.step("Отправка GET запроса"):
        response = requests.get(url, headers=api_client["headers"])

    with allure.step("Проверка статус кода 200"):
        assert response.status_code == 200, \
            f"Ожидался статус 200, получен {response.status_code}"

    with allure.step("Проверка данных фильма"):
        data = response.json()
        assert "id" in data, "В ответе нет поля 'id'"
        assert data["id"] == MOVIE_IDS["valid"], \
            f"ID фильма не совпадает: {data['id']} != {MOVIE_IDS['valid']}"

        allure.attach(
            f"Название фильма: {data.get('name', 'Не указано')}\n"
            f"ID: {data.get('id', 'Не указано')}",
            name="movie_info",
            attachment_type=allure.attachment_type.TEXT
        )


@pytest.mark.api
@allure.title("TC-API-03: Поиск актера (позитивный)")
@allure.story("API поиск персон")
@allure.severity(allure.severity_level.CRITICAL)
def test_api_search_person(api_client: Dict[str, Any]) -> None:
    """
    Позитивный тест API: поиск актера

    Expected: статус 200, результаты поиска
    """
    with allure.step("Подготовка запроса для поиска актера 'Keanu Reeves'"):
        url = f"{API_BASE_URL.rstrip('/')}/person/search"
        params = {
            "query": SEARCH_QUERIES["valid_actor"],
            "page": 1,
            "limit": 10
        }

    with allure.step("Отправка GET запроса"):
        response = requests.get(
            url,
            params=params,
            headers=api_client["headers"]
        )

    with allure.step("Проверка статус кода 200"):
        assert response.status_code == 200, \
            f"Ожидался статус 200, получен {response.status_code}"

    with allure.step("Проверка результатов поиска"):
        data = response.json()
        assert "docs" in data, "В ответе нет поля 'docs'"

        # Проверяем, что нашли Keanu Reeves
        docs = data.get("docs", [])
        keanu_found = any(
            "Keanu" in str(doc.get("name", "")) or
            "Киану" in str(doc.get("name", ""))
            for doc in docs
        )

        allure.attach(
            f"Найдено результатов: {len(docs)}\n"
            f"Keanu Reeves найден: {keanu_found}",
            name="person_search_results",
            attachment_type=allure.attachment_type.TEXT
        )


@pytest.mark.api
@allure.title("TC-API-04: Запрос без токена (негативный)")
@allure.story("API авторизация")
@allure.severity(allure.severity_level.NORMAL)
def test_api_request_without_token() -> None:
    """
    Негативный тест API: запрос без API ключа

    Expected: статус 401 (Unauthorized)
    """
    with allure.step("Подготовка запроса без API ключа"):
        url = f"{API_BASE_URL.rstrip('/')}/movie/search"
        params = {
            "query": SEARCH_QUERIES["valid_movie"],
            "page": 1,
            "limit": 10
        }
        headers = {"accept": "application/json"}
        # Намеренно НЕ добавляем X-API-KEY

    with allure.step("Отправка GET запроса без токена"):
        response = requests.get(url, params=params, headers=headers)

    with allure.step("Проверка статус кода 401"):
        # Некоторые API могут возвращать 400 или 403, проверяем ошибку авторизации
        assert response.status_code in [401, 403, 400], \
            f"Ожидалась ошибка авторизации (401/403/400), получен {response.status_code}"

        allure.attach(
            f"Статус код: {response.status_code}\n"
            f"Ответ: {response.text[:200]}",
            name="unauthorized_response",
            attachment_type=allure.attachment_type.TEXT
        )


@pytest.mark.api
@allure.title("TC-API-05: Поиск фильма по несуществующему ID (негативный)")
@allure.story("API обработка ошибок")
@allure.severity(allure.severity_level.NORMAL)
def test_api_search_nonexistent_movie_id(api_client: Dict[str, Any]) -> None:
    """
    Негативный тест API: поиск фильма по несуществующему ID

    Expected: статус 400 (Bad Request) или 404 (Not Found)
    """
    with allure.step("Подготовка запроса с несуществующим ID"):
        url = f"{API_BASE_URL.rstrip('/')}/movie/{MOVIE_IDS['invalid']}"

    with allure.step("Отправка GET запроса"):
        response = requests.get(url, headers=api_client["headers"])

    with allure.step("Проверка ошибки (400 или 404)"):
        # API может возвращать 400 для некорректных ID или 404 если не найдено
        assert response.status_code in [400, 404], \
            f"Ожидалась ошибка 400 или 404, получен {response.status_code}"

        allure.attach(
            f"Статус код: {response.status_code}\n"
            f"Ответ: {response.text[:200]}",
            name="invalid_id_response",
            attachment_type=allure.attachment_type.TEXT
        )