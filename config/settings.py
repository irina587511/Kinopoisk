"""
Настройки проекта для тестирования Кинопоиска
"""

# URL для тестирования
BASE_URL = "https://www.kinopoisk.ru"
HD_BASE_URL = "https://hd.kinopoisk.ru/"
API_BASE_URL = "https://api.kinopoisk.dev/v1.4/"
GRAPHQL_URL = "https://graphql.kinopoisk.ru/graphql/"

# Таймауты
DEFAULT_TIMEOUT = 20
SHORT_TIMEOUT = 5
LONG_TIMEOUT = 30

# Пути
SCREENSHOTS_DIR = "screenshots"
ALLURE_RESULTS_DIR = "allure-results"

# Тестовые данные для поиска
SEARCH_QUERIES = {
    "valid_movie": "king",
    "valid_actor": "Keanu Reeves",
    "invalid_movie": "fkjhskfjhgbtkgiglfdiwebwivhgnkb",
    "invalid_actor": "Rjhbxhjdhv Pjmnkj",
    "empty": "",
    "spaces": "   "
}

# ID фильмов для тестирования
MOVIE_IDS = {
    "valid": 5089022,  # Довод
    "invalid": 5089022222222,
    "too_small": 1
}