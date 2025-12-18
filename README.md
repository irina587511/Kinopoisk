# Kinopoisk

Ссылка на тест-план (Финальный проект) в Yonote:
https://otchety.yonote.ru/doc/finalnyj-proekt-po-ruchnomu-testirovaniyu-Z9wOYY0giD

Доступ:

Irina587511@gmail.com

MzT7q!UzW-F9SmH


# Автоматизация тестирования Кинопоиска

Финальный проект по автоматизации тестирования UI и API сайта Кинопоиск.

# Автоматизация тестирования Кинопоиска

Финальный проект по автоматизации тестирования UI и API сайта Кинопоиск.


Ссылка на тест-план (Финальный проект) в Yonote:
https://otchety.yonote.ru/doc/finalnyj-proekt-po-ruchnomu-testirovaniyu-Z9wOYY0giD
Доступ:
Irina587511@gmail.com
MzT7q!UzW-F9SmH


## Структура проекта
kinopoisk-automation-final/
├── config/ # Конфигурационные файлы
├── tests/ # UI и API тесты
├── utils/ # Вспомогательные утилиты
├── .gitignore # Игнорируемые файлы
├── requirements.txt # Зависимости
└── README.md # Документация

text

## Установка и настройка

1. **Клонирование репозитория:**
```bash
git clone <ваш-репозиторий>
cd kinopoisk-automation-final
Установка зависимостей:

bash
pip install -r requirements.txt
Настройка API ключа:

Создайте файл config/credentials.py

Добавьте ваш API ключ:

python
API_KEY = "27HS79C-JMNMKVM-MKKCCNK-D7H6NTR"
Запуск тестов
Режимы запуска:
Все тесты:

bash
pytest
Только UI тесты:

bash
pytest -m "ui"
Только API тесты:

bash
pytest -m "api"
Дополнительные опции:
С отчетом Allure:

bash
pytest --alluredir=allure-results
allure serve allure-results
С HTML отчетом:

bash
pytest --html=report.html
Параллельный запуск:

bash
pytest -n auto
pytest -n auto
