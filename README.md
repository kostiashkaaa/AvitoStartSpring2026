# Тестовое задание для стажёра QA (весна 2026)

## Структура проекта

```
AvitoStartTaskSping/
├── api_tests/
│   ├── conftest.py             # BASE_URL и вспомогательные функции
│   ├── test_create_item.py     # Тесты создания объявления
│   ├── test_get_item.py        # Тесты получения объявления по id
│   ├── test_get_seller_items.py# Тесты списка объявлений продавца
│   ├── test_get_statistic.py   # Тесты статистики
│   └── test_e2e.py             # Сквозные E2E тесты
├── requirements.txt            # Зависимости
├── pytest.ini                  # Настройки pytest
├── TESTCASES.md                # Тест-кейсы для API (Задание 2.1)
├── BUGS.md                     # Описание найденных багов API
└── ZADANIE1_BUGS.md            # Баги со скриншота (Задание 1)
```

## Установка

```bash
pip install -r requirements.txt
```

## Запуск тестов

```bash
# Все тесты
pytest

# Конкретный файл
pytest api_tests/test_create_item.py -v
```

## Примечания

- `sellerID` в тестах генерируется случайно в диапазоне **111111–999999**.
- Тесты, падающие из-за бага сервера, помечены `[BUG]` в тексте ошибки.
- Все найденные баги описаны в `BUGS.md`.
