# Баг-репорты (API)

Список найденных дефектов в API `https://qa-internship.avito.com` при автоматизированном тестировании.

---

## 1. POST /api/1/item принимает пустое поле name
**Описание:** При создании объявления с пустым именем (`name: ""`) сервер возвращает код 200 и создаёт объявление.

**Шаги воспроизведения:**
```bash
curl -X POST https://qa-internship.avito.com/api/1/item \
  -H 'Content-Type: application/json' \
  -d '{"sellerId": 123456, "name": "", "price": 1000, "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}}'
```
**Фактический результат:** HTTP 200, объявление создано.
**Ожидаемый результат:** HTTP 400 Bad Request, так как название — обязательное поле.
**Приоритет:** Высокий

---

## 2. POST /api/1/item принимает отрицательную цену
**Описание:** Сервер позволяет создать объявление с отрицательной ценой `price: -1`.

**Шаги воспроизведения:**
```bash
curl -X POST https://qa-internship.avito.com/api/1/item \
  -H 'Content-Type: application/json' \
  -d '{"sellerId": 123456, "name": "Test", "price": -1, "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}}'
```
**Фактический результат:** HTTP 200, ошибка валидации отсутствует.
**Ожидаемый результат:** HTTP 400 Bad Request, цена не может быть меньше нуля.
**Приоритет:** Высокий

---

## 3. POST /api/1/item принимает отрицательную статистику
**Описание:** При передаче, например, `likes: -5`, сервер успешно создает объявление.

**Шаги воспроизведения:**
```bash
curl -X POST https://qa-internship.avito.com/api/1/item \
  -H 'Content-Type: application/json' \
  -d '{"sellerId": 123456, "name": "Test", "price": 100, "statistics": {"likes": -5, "viewCount": 0, "contacts": 0}}'
```
**Фактический результат:** HTTP 200.
**Ожидаемый результат:** HTTP 400, статистика не может быть отрицательной.
**Приоритет:** Средний

---

## 4. POST /api/1/item принимает sellerId = 0
**Описание:** `sellerId: 0` создаётся без ошибки, хотя по документации это число из диапазона 111111–999999.

**Шаги воспроизведения:**
```bash
curl -X POST https://qa-internship.avito.com/api/1/item \
  -H 'Content-Type: application/json' \
  -d '{"sellerId": 0, "name": "Test", "price": 100, "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}}'
```
**Фактический результат:** HTTP 200.
**Ожидаемый результат:** HTTP 400.
**Приоритет:** Средний

---

## 5. POST /api/1/item успешно работает без обязательного поля name
**Описание:** Если вообще не отправить поле `name`, запрос проходит успешно.

**Шаги воспроизведения:**
```bash
curl -X POST https://qa-internship.avito.com/api/1/item \
  -H 'Content-Type: application/json' \
  -d '{"sellerId": 123456, "price": 1000, "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}}'
```
**Фактический результат:** HTTP 200.
**Ожидаемый результат:** HTTP 400, требуется обязательное поле `name`.
**Приоритет:** Высокий

---

## 6. POST /api/1/item успешно работает без поля price
**Описание:** Аналогично с полем `price` — если его не передать, сервер отдаёт 200.

**Шаги воспроизведения:**
```bash
curl -X POST https://qa-internship.avito.com/api/1/item \
  -H 'Content-Type: application/json' \
  -d '{"sellerId": 123456, "name": "Test", "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}}'
```
**Фактический результат:** HTTP 200.
**Ожидаемый результат:** HTTP 400, требуется поле `price`.
**Приоритет:** Высокий

---

## 7. POST /api/1/item не проверяет тип поля price (принимает строку)
**Описание:** Сервер проглатывает строку `"not_a_number"` в поле `price`.

**Шаги воспроизведения:**
```bash
curl -X POST https://qa-internship.avito.com/api/1/item \
  -H 'Content-Type: application/json' \
  -d '{"sellerId": 123456, "name": "Test", "price": "not_a_number", "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}}'
```
**Фактический результат:** HTTP 200.
**Ожидаемый результат:** HTTP 400, ожидался числовой тип данных.
**Приоритет:** Высокий

---

## 8. GET /api/1/statistic/:id выдаёт 400 для правильного UUID
**Описание:** Запрос статистики созданного объявления ругается на "некорректный идентификатор".

**Фактический результат:** HTTP 400 на заведомо правильный `id`.
**Ожидаемый результат:** HTTP 200 со статистикой.
**Приоритет:** Критический (ручка статистики не работает)

---

## 9. GET /api/1/:sellerId/item возвращает пустоту или 404
**Описание:** После создания объявлений ручка получения всех товаров продавца отдаёт `[]` (или иногда 404).

**Фактический результат:** `[]` или 404.
**Ожидаемый результат:** Массив созданных объявлений продавца.
**Приоритет:** Критический

---

## 10. POST /api/1/item работает без sellerId
**Описание:** Объявление создаётся без привязки к продавцу (отсутствует `sellerId`).

**Шаги воспроизведения:**
```bash
curl -X POST https://qa-internship.avito.com/api/1/item \
  -H 'Content-Type: application/json' \
  -d '{"name": "Test", "price": 100, "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}}'
```
**Фактический результат:** HTTP 200.
**Ожидаемый результат:** HTTP 400.
**Приоритет:** Высокий

---

## 11. POST /api/1/item падает 400 ошибкой при цене price=0
**Описание:** Если передать `price: 0` (хотим разместить товар бесплатно), получаем ошибку сервера. Но при этом `price: -100` проходит на ура.

**Шаги воспроизведения:**
```bash
curl -X POST https://qa-internship.avito.com/api/1/item \
  -H 'Content-Type: application/json' \
  -d '{"sellerId": 123456, "name": "Free item", "price": 0, "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}}'
```
**Фактический результат:** HTTP 400 Bad Request.
**Ожидаемый результат:** HTTP 200.
**Приоритет:** Средний
