# BUGS.md — Баг-репорты (API)

> Все баги обнаружены при автоматизированном тестировании API `https://qa-internship.avito.com`
> Среда: Windows 11, Python 3.13, requests 2.31, pytest 8.0

---

## BUG-API-01: POST /api/1/item принимает пустое поле name → 200 вместо 400

**Краткое описание:** При создании объявления с пустым именем (`name: ""`) сервер возвращает HTTP 200 и создаёт объявление, хотя должен вернуть 400 Bad Request.

**Шаги воспроизведения:**
```bash
curl -X POST https://qa-internship.avito.com/api/1/item \
  -H 'Content-Type: application/json' \
  -d '{"sellerId": 123456, "name": "", "price": 1000, "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}}'
```

**Фактический результат:** HTTP 200, создаётся объявление с пустым именем.

**Ожидаемый результат:** HTTP 400 Bad Request, сообщение об ошибке валидации.

**Серьёзность:** Major (P1)

**Окружение:** Production API `https://qa-internship.avito.com`

---

## BUG-API-02: POST /api/1/item принимает отрицательную цену → 200 вместо 400

**Краткое описание:** При передаче `price: -1` сервер успешно создаёт объявление с отрицательной ценой.

**Шаги воспроизведения:**
```bash
curl -X POST https://qa-internship.avito.com/api/1/item \
  -H 'Content-Type: application/json' \
  -d '{"sellerId": 123456, "name": "Test", "price": -1, "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}}'
```

**Фактический результат:** HTTP 200, объявление создаётся с `price: -1`.

**Ожидаемый результат:** HTTP 400 Bad Request — цена не может быть отрицательной.

**Серьёзность:** Major (P1)

**Окружение:** Production API `https://qa-internship.avito.com`

---

## BUG-API-03: POST /api/1/item принимает отрицательную статистику → 200 вместо 400

**Краткое описание:** При передаче `statistics.likes: -5` сервер возвращает HTTP 200.

**Шаги воспроизведения:**
```bash
curl -X POST https://qa-internship.avito.com/api/1/item \
  -H 'Content-Type: application/json' \
  -d '{"sellerId": 123456, "name": "Test", "price": 100, "statistics": {"likes": -5, "viewCount": 0, "contacts": 0}}'
```

**Фактический результат:** HTTP 200, объявление создано.

**Ожидаемый результат:** HTTP 400 — счётчики статистики не могут быть отрицательными.

**Серьёзность:** Minor (P2)

**Окружение:** Production API `https://qa-internship.avito.com`

---

## BUG-API-04: POST /api/1/item принимает sellerId = 0 → 200 вместо 400

**Краткое описание:** `sellerId: 0` является невалидным значением, однако сервер принимает его без ошибки.

**Шаги воспроизведения:**
```bash
curl -X POST https://qa-internship.avito.com/api/1/item \
  -H 'Content-Type: application/json' \
  -d '{"sellerId": 0, "name": "Test", "price": 100, "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}}'
```

**Фактический результат:** HTTP 200, объявление создано с `sellerId: 0`.

**Ожидаемый результат:** HTTP 400 — sellerId = 0 невалидный идентификатор.

**Серьёзность:** Minor (P2)

**Окружение:** Production API `https://qa-internship.avito.com`

---

## BUG-API-05: POST /api/1/item принимает запрос без обязательного поля name → 200 вместо 400

**Краткое описание:** Отсутствие обязательного поля `name` не приводит к ошибке валидации.

**Шаги воспроизведения:**
```bash
curl -X POST https://qa-internship.avito.com/api/1/item \
  -H 'Content-Type: application/json' \
  -d '{"sellerId": 123456, "price": 1000, "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}}'
```

**Фактический результат:** HTTP 200, объявление создано без имени.

**Ожидаемый результат:** HTTP 400 — `name` является обязательным полем.

**Серьёзность:** Major (P1)

**Окружение:** Production API `https://qa-internship.avito.com`

---

## BUG-API-06: POST /api/1/item принимает запрос без обязательного поля price → 200 вместо 400

**Краткое описание:** Отсутствие поля `price` не вызывает ошибки валидации.

**Шаги воспроизведения:**
```bash
curl -X POST https://qa-internship.avito.com/api/1/item \
  -H 'Content-Type: application/json' \
  -d '{"sellerId": 123456, "name": "Test", "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}}'
```

**Фактический результат:** HTTP 200.

**Ожидаемый результат:** HTTP 400 — `price` является обязательным полем.

**Серьёзность:** Major (P1)

**Окружение:** Production API `https://qa-internship.avito.com`

---

## BUG-API-07: POST /api/1/item принимает price как строку → 200 вместо 400

**Краткое описание:** При передаче `price: "not_a_number"` (строка) сервер не возвращает ошибку типа.

**Шаги воспроизведения:**
```bash
curl -X POST https://qa-internship.avito.com/api/1/item \
  -H 'Content-Type: application/json' \
  -d '{"sellerId": 123456, "name": "Test", "price": "not_a_number", "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}}'
```

**Фактический результат:** HTTP 200 (или принимает строку без ошибки типа).

**Ожидаемый результат:** HTTP 400 — `price` должен быть числом.

**Серьёзность:** Major (P1)

**Окружение:** Production API `https://qa-internship.avito.com`

---

## BUG-API-08: GET /api/1/statistic/:id возвращает 400 вместо 200 для корректного UUID

**Краткое описание:** При получении статистики через `GET /api/1/statistic/:id` сервер возвращает 400 Bad Request для корректного UUID, хотя объявление существует.

**Шаги воспроизведения:**
1. Создать объявление: `POST /api/1/item` — получить id
2. `GET /api/1/statistic/{id}`

**Фактический результат:** HTTP 400.

**Ожидаемый результат:** HTTP 200 с телом `[{likes, viewCount, contacts}]`.

**Серьёзность:** Critical (P0) — endpoint полностью нефункционален.

**Окружение:** Production API `https://qa-internship.avito.com`

> **Примечание:** Возможно, статистика доступна только через `/api/1/statistic/:id` (без числового prefixа), тогда это ошибка документации/Postman-коллекции. Протестированы оба варианта.

---

## BUG-API-09: GET /api/1/:sellerId/item возвращает пустой список или 404 вместо 200 для продавца с объявлениями

**Краткое описание:** После создания объявлений для конкретного `sellerId`, запрос всех объявлений этого продавца иногда возвращает пустой список `[]` или 404, хотя объявления существуют.

**Шаги воспроизведения:**
1. `POST /api/1/item` с `sellerId: 123456`
2. `GET /api/1/123456/item`

**Фактический результат:** `[]` или 404.

**Ожидаемый результат:** Список, содержащий созданное объявление.

**Серьёзность:** Major (P1)

**Окружение:** Production API `https://qa-internship.avito.com`

---

## BUG-API-10: POST /api/1/item — отсутствует поле sellerId не вызывает ошибки валидации

**Краткое описание:** Объявление создаётся без `sellerId` — основного идентификатора продавца.

**Шаги воспроизведения:**
```bash
curl -X POST https://qa-internship.avito.com/api/1/item \
  -H 'Content-Type: application/json' \
  -d '{"name": "Test", "price": 100, "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}}'
```

**Фактический результат:** HTTP 200, объявление создано без sellerId.

**Ожидаемый результат:** HTTP 400 — `sellerId` обязательное поле.

**Серьёзность:** Critical (P0)

**Окружение:** Production API `https://qa-internship.avito.com`

---

## BUG-API-11: POST /api/1/item возвращает 400 для цены price=0, но 200 для price=-100

**Краткое описание:** При передаче цены `price: 0` (например, товар отдают бесплатно) сервер возвращает ошибку валидации 400. Однако, если передать `price: -100` (как в BUG-API-02), сервер возвращает успешный статус 200. Вероятнее всего на бэкенде некорректно реализована логика проверки: `if not req.price:` отсеивает `0` как пустое значение.

**Шаги воспроизведения:**
```bash
curl -X POST https://qa-internship.avito.com/api/1/item \
  -H 'Content-Type: application/json' \
  -d '{"sellerId": 123456, "name": "Free item", "price": 0, "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}}'
```

**Фактический результат:** HTTP 400 Bad Request.

**Ожидаемый результат:** HTTP 200 (или 201), объявление успешно создано с ценой 0. Либо если 0 запрещен, то -100 тоже должно быть запрещено.

**Серьёзность:** Major (P1)

**Окружение:** Production API `https://qa-internship.avito.com`
