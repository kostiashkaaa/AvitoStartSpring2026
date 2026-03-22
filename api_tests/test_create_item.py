import random
import requests

BASE_URL = "https://qa-internship.avito.com"


def make_payload(seller_id=None, name="Котёнок персидский", price=5000):
    return {
        "sellerID": seller_id or random.randint(111111, 999999),
        "name": name,
        "price": price,
        "statistics": {
            "likes": 0,
            "viewCount": 0,
            "contacts": 0,
        },
    }


# --- Позитивные тесты ---

def test_create_item_success():
    response = requests.post(f"{BASE_URL}/api/1/item", json=make_payload(), timeout=10)
    assert response.status_code == 200


def test_create_item_response_has_id():
    response = requests.post(f"{BASE_URL}/api/1/item", json=make_payload(), timeout=10)
    assert response.status_code == 200
    data = response.json()
    item_id = data.get("id") or data.get("status")
    assert item_id is not None, f"Нет id в ответе: {data}"
    assert len(str(item_id)) > 0, "id не должен быть пустым"


def test_create_item_two_requests_give_different_ids():
    payload = make_payload()
    response1 = requests.post(f"{BASE_URL}/api/1/item", json=payload, timeout=10)
    response2 = requests.post(f"{BASE_URL}/api/1/item", json=payload, timeout=10)
    assert response1.status_code == 200
    assert response2.status_code == 200
    id1 = response1.json().get("id") or response1.json().get("status")
    id2 = response2.json().get("id") or response2.json().get("status")
    assert id1 != id2, "Каждое объявление должно получать уникальный id"


def test_create_item_with_zero_price():
    payload = make_payload(price=0)
    response = requests.post(f"{BASE_URL}/api/1/item", json=payload, timeout=10)
    assert response.status_code == 200


def test_create_item_response_time_is_acceptable():
    response = requests.post(f"{BASE_URL}/api/1/item", json=make_payload(), timeout=10)
    assert response.elapsed.total_seconds() < 3, (
        f"Слишком долгий ответ: {response.elapsed.total_seconds():.2f}с"
    )


# --- Негативные тесты ---

def test_create_item_without_name_returns_error():
    """[BUG: сервер возвращает 200 вместо 400]"""
    payload = make_payload()
    del payload["name"]
    response = requests.post(f"{BASE_URL}/api/1/item", json=payload, timeout=10)
    assert response.status_code == 400, (
        f"[BUG] Ожидался 400 при отсутствии name, получили {response.status_code}"
    )


def test_create_item_without_price_returns_error():
    """[BUG: сервер возвращает 200 вместо 400]"""
    payload = make_payload()
    del payload["price"]
    response = requests.post(f"{BASE_URL}/api/1/item", json=payload, timeout=10)
    assert response.status_code == 400, (
        f"[BUG] Ожидался 400 при отсутствии price, получили {response.status_code}"
    )


def test_create_item_with_negative_price_returns_error():
    """[BUG: сервер возвращает 200 вместо 400]"""
    payload = make_payload(price=-100)
    response = requests.post(f"{BASE_URL}/api/1/item", json=payload, timeout=10)
    assert response.status_code == 400, (
        f"[BUG] Ожидался 400 для price=-100, получили {response.status_code}"
    )


def test_create_item_with_empty_name_returns_error():
    """[BUG: сервер возвращает 200 вместо 400]"""
    payload = make_payload(name="")
    response = requests.post(f"{BASE_URL}/api/1/item", json=payload, timeout=10)
    assert response.status_code == 400, (
        f"[BUG] Ожидался 400 для пустого name, получили {response.status_code}"
    )


def test_create_item_with_string_price_returns_error():
    payload = make_payload()
    payload["price"] = "дорого"
    response = requests.post(f"{BASE_URL}/api/1/item", json=payload, timeout=10)
    assert response.status_code == 400, (
        f"[BUG] Ожидался 400 для price='дорого', получили {response.status_code}"
    )
