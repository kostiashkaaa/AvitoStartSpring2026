import uuid
import random
import requests

BASE_URL = "https://qa-internship.avito.com"


def create_item_with_stats(likes=5, view_count=20, contacts=3):
    seller_id = random.randint(111111, 999999)
    payload = {
        "sellerId": seller_id,
        "name": "Объявление со статистикой",
        "price": 1500,
        "statistics": {
            "likes": likes,
            "viewCount": view_count,
            "contacts": contacts,
        },
    }
    response = requests.post(f"{BASE_URL}/api/1/item", json=payload, timeout=10)
    assert response.status_code == 200
    data = response.json()
    item_id = data.get("id")
    if not item_id and "status" in data:
        item_id = data["status"].split(" - ")[-1]
    return item_id, payload


#Позитивные тесты

def test_get_statistic_returns_200():
    item_id, _ = create_item_with_stats()
    response = requests.get(f"{BASE_URL}/api/1/statistic/{item_id}", timeout=10)
    assert response.status_code == 200, (
        f"[BUG] Ожидался 200 для статистики, получили {response.status_code}: {response.text}"
    )


def test_get_statistic_returns_list():
    item_id, _ = create_item_with_stats()
    response = requests.get(f"{BASE_URL}/api/1/statistic/{item_id}", timeout=10)
    assert response.status_code == 200
    assert isinstance(response.json(), list), "Ответ должен быть массивом"


def test_get_statistic_has_required_fields():
    item_id, _ = create_item_with_stats()
    response = requests.get(f"{BASE_URL}/api/1/statistic/{item_id}", timeout=10)
    assert response.status_code == 200
    stat = response.json()[0]
    assert "likes" in stat, f"Нет поля likes в статистике: {stat}"
    assert "viewCount" in stat, f"Нет поля viewCount в статистике: {stat}"
    assert "contacts" in stat, f"Нет поля contacts в статистике: {stat}"


def test_get_statistic_values_match_created():
    item_id, payload = create_item_with_stats(likes=7, view_count=42, contacts=9)
    response = requests.get(f"{BASE_URL}/api/1/statistic/{item_id}", timeout=10)
    assert response.status_code == 200
    stat = response.json()[0]
    expected = payload["statistics"]
    assert stat["likes"] == expected["likes"], f"likes: {stat['likes']} != {expected['likes']}"
    assert stat["viewCount"] == expected["viewCount"], f"viewCount: {stat['viewCount']} != {expected['viewCount']}"
    assert stat["contacts"] == expected["contacts"], f"contacts: {stat['contacts']} != {expected['contacts']}"


# --- Негативные тесты ---

def test_get_statistic_nonexistent_id_returns_404():
    fake_id = str(uuid.uuid4())
    response = requests.get(f"{BASE_URL}/api/1/statistic/{fake_id}", timeout=10)
    assert response.status_code == 404, (
        f"Ожидался 404, получили {response.status_code}"
    )


def test_get_statistic_invalid_id_returns_400():
    response = requests.get(f"{BASE_URL}/api/1/statistic/не-uuid-строка", timeout=10)
    assert response.status_code == 400, (
        f"Ожидался 400 для не-UUID, получили {response.status_code}"
    )
