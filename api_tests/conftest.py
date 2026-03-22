import random
import requests

BASE_URL = "https://qa-internship.avito.com"


def random_seller_id():
    return random.randint(111111, 999999)


def create_item(seller_id=None, name="Test Item", price=1000):
    payload = {
        "sellerId": seller_id or random_seller_id(),
        "name": name,
        "price": price,
        "statistics": {
            "likes": 5,
            "viewCount": 10,
            "contacts": 2,
        },
    }
    response = requests.post(f"{BASE_URL}/api/1/item", json=payload, timeout=10)
    assert response.status_code == 200, f"Не удалось создать объявление: {response.text}"
    data = response.json()
    item_id = data.get("id")
    if not item_id and "status" in data:
        item_id = data["status"].split(" - ")[-1]
    return item_id, payload
