import os

# API ключ из переменной окружения или заданный явно
API_KEY = os.getenv("KP_API_KEY", "27HS79C-JMNMKVM-MKKCCNK-D7H6NTR")

# Данные для авторизации (если нужны)
TEST_EMAIL = os.getenv("KP_TEST_EMAIL", "") # не могу пока ввести валидные данные,
# т.к. заблокирована
TEST_PASSWORD = os.getenv("KP_TEST_PASSWORD", "") # не могу пока ввести валидные данные,
# т.к. заблокирована

# Cookie для авторизации (опционально)
AUTH_COOKIES = {
    # Здесь будут куки после авторизации
}