import uuid
import random
import requests

BASE_URL = "https://qa-internship.avito.com"


def create_test_item():
    payload = {
        "sellerID": random.randint(111111, 999999),
        "name": "Тестовое объявление",
        "price": 2500,
        "statistics": {"likes": 3, "viewCount": 15, "contacts": 1},
    }
    response = requests.post(f"{BASE_URL}/api/1/item", json=payload, timeout=10)
    assert response.status_code == 200
    data = response.json()
    item_id = data.get("id") or data.get("status")
    return item_id, payload


#Позитивные тесты

def test_get_item_by_id_returns_200():
    item_id, _ = create_test_item()
    response = requests.get(f"{BASE_URL}/api/1/item/{item_id}", timeout=10)
    assert response.status_code == 200


def test_get_item_response_is_list():
    item_id, _ = create_test_item()
    response = requests.get(f"{BASE_URL}/api/1/item/{item_id}", timeout=10)
    assert response.status_code == 200
    assert isinstance(response.json(), list), "Ответ должен быть массивом"


def test_get_item_has_correct_fields():
    item_id, _ = create_test_item()
    response = requests.get(f"{BASE_URL}/api/1/item/{item_id}", timeout=10)
    assert response.status_code == 200
    item = response.json()[0]
    assert "id" in item
    assert "sellerId" in item
    assert "name" in item
    assert "price" in item
    assert "statistics" in item
    assert "createdAt" in item


def test_get_item_name_matches_created():
    item_id, payload = create_test_item()
    response = requests.get(f"{BASE_URL}/api/1/item/{item_id}", timeout=10)
    assert response.status_code == 200
    item = response.json()[0]
    assert item["name"] == payload["name"], (
        f"Ожидалось '{payload['name']}', получили '{item['name']}'"
    )


def test_get_item_price_matches_created():
    item_id, payload = create_test_item()
    response = requests.get(f"{BASE_URL}/api/1/item/{item_id}", timeout=10)
    assert response.status_code == 200
    item = response.json()[0]
    assert item["price"] == payload["price"], (
        f"Ожидалась цена {payload['price']}, получили {item['price']}"
    )


#Негативные тесты

def test_get_item_with_nonexistent_uuid_returns_404():
    fake_id = str(uuid.uuid4())
    response = requests.get(f"{BASE_URL}/api/1/item/{fake_id}", timeout=10)
    assert response.status_code == 404, (
        f"Ожидался 404, получили {response.status_code}"
    )


def test_get_item_with_invalid_id_returns_400():
    response = requests.get(f"{BASE_URL}/api/1/item/это-не-uuid", timeout=10)
    assert response.status_code == 400, (
        f"Ожидался 400 для не-UUID, получили {response.status_code}"
    )


def test_get_item_with_number_id_returns_400():
    response = requests.get(f"{BASE_URL}/api/1/item/12345", timeout=10)
    assert response.status_code == 400, (
        f"Ожидался 400 для числового id, получили {response.status_code}"
    )
