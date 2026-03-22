import random
import requests

BASE_URL = "https://qa-internship.avito.com"


def test_create_then_get_by_id():
    seller_id = random.randint(111111, 999999)
    payload = {
        "sellerId": seller_id,
        "name": "E2E Тест объявление",
        "price": 7000,
        "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
    }

    #Шаг 1: Создать объявление
    create_response = requests.post(f"{BASE_URL}/api/1/item", json=payload, timeout=10)
    assert create_response.status_code == 200, "Шаг 1: Не удалось создать объявление"
    item_id = create_response.json().get("id")
    if not item_id and "status" in create_response.json():
        item_id = create_response.json().get("status").split(" - ")[-1]

    #Шаг 2: Получить объявление по id
    get_response = requests.get(f"{BASE_URL}/api/1/item/{item_id}", timeout=10)
    assert get_response.status_code == 200, "Шаг 2: Не удалось получить объявление"
    item = get_response.json()[0]

    assert item["id"] == item_id
    assert item["name"] == payload["name"]
    assert item["price"] == payload["price"]
    assert item["sellerId"] == seller_id


def test_create_then_find_in_seller_list():
    seller_id = random.randint(111111, 999999)
    payload = {
        "sellerId": seller_id,
        "name": "Объявление в списке",
        "price": 500,
        "statistics": {"likes": 1, "viewCount": 1, "contacts": 1},
    }

    #Шаг 1: Создать
    create_response = requests.post(f"{BASE_URL}/api/1/item", json=payload, timeout=10)
    assert create_response.status_code == 200
    item_id = create_response.json().get("id")
    if not item_id and "status" in create_response.json():
        item_id = create_response.json().get("status").split(" - ")[-1]

    #Шаг 2: Получить список продавца
    list_response = requests.get(f"{BASE_URL}/api/1/{seller_id}/item", timeout=10)
    assert list_response.status_code == 200

    #Шаг 3: Объявление должно быть в списке
    item_ids = [item["id"] for item in list_response.json()]
    assert item_id in item_ids, (
        f"Созданное объявление {item_id} не найдено в списке продавца {seller_id}"
    )


def test_create_then_get_statistics():
    seller_id = random.randint(111111, 999999)
    stats = {"likes": 5, "viewCount": 30, "contacts": 2}
    payload = {
        "sellerId": seller_id,
        "name": "Объявление для статистики",
        "price": 1200,
        "statistics": stats,
    }

    #Шаг 1: Создать
    create_response = requests.post(f"{BASE_URL}/api/1/item", json=payload, timeout=10)
    assert create_response.status_code == 200
    item_id = create_response.json().get("id")
    if not item_id and "status" in create_response.json():
        item_id = create_response.json().get("status").split(" - ")[-1]

    #Шаг 2: Получить статистику
    stat_response = requests.get(f"{BASE_URL}/api/1/statistic/{item_id}", timeout=10)
    assert stat_response.status_code == 200, (
        f"[BUG] Статистика вернула {stat_response.status_code} вместо 200"
    )
    stat = stat_response.json()[0]
    assert stat["likes"] == stats["likes"]
    assert stat["viewCount"] == stats["viewCount"]
    assert stat["contacts"] == stats["contacts"]
