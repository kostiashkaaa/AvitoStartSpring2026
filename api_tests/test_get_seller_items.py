import random
import requests

BASE_URL = "https://qa-internship.avito.com"


def create_item_for_seller(seller_id):
    payload = {
        "sellerId": seller_id,
        "name": "Объявление для продавца",
        "price": 3000,
        "statistics": {"likes": 1, "viewCount": 5, "contacts": 2},
    }
    response = requests.post(f"{BASE_URL}/api/1/item", json=payload, timeout=10)
    assert response.status_code == 200
    data = response.json()
    item_id = data.get("id")
    if not item_id and "status" in data:
        item_id = data["status"].split(" - ")[-1]
    return item_id


#Позитивные тесты

def test_get_seller_items_returns_200():
    seller_id = random.randint(111111, 999999)
    create_item_for_seller(seller_id)
    response = requests.get(f"{BASE_URL}/api/1/{seller_id}/item", timeout=10)
    assert response.status_code == 200


def test_get_seller_items_returns_list():
    seller_id = random.randint(111111, 999999)
    create_item_for_seller(seller_id)
    response = requests.get(f"{BASE_URL}/api/1/{seller_id}/item", timeout=10)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_created_item_appears_in_seller_list():
    seller_id = random.randint(111111, 999999)
    item_id = create_item_for_seller(seller_id)
    response = requests.get(f"{BASE_URL}/api/1/{seller_id}/item", timeout=10)
    assert response.status_code == 200
    ids = [item["id"] for item in response.json()]
    assert item_id in ids, f"Объявление {item_id} не найдено в списке продавца"


def test_seller_items_all_belong_to_seller():
    seller_id = random.randint(111111, 999999)
    create_item_for_seller(seller_id)
    response = requests.get(f"{BASE_URL}/api/1/{seller_id}/item", timeout=10)
    assert response.status_code == 200
    for item in response.json():
        assert item["sellerId"] == seller_id, (
            f"Объявление {item['id']} принадлежит продавцу {item['sellerId']}, "
            f"ожидался {seller_id}"
        )


def test_seller_items_no_crossover():
    seller_a = random.randint(111111, 500000)
    seller_b = random.randint(500001, 999999)
    item_id_a = create_item_for_seller(seller_a)

    response = requests.get(f"{BASE_URL}/api/1/{seller_b}/item", timeout=10)
    assert response.status_code == 200
    ids_b = [item["id"] for item in response.json()]
    assert item_id_a not in ids_b, "Объявление продавца А попало в список продавца Б!"


#Негативные тесты

def test_seller_items_invalid_seller_id_returns_400():
    response = requests.get(f"{BASE_URL}/api/1/не-число/item", timeout=10)
    assert response.status_code == 400, (
        f"Ожидался 400 для нечислового sellerId, получили {response.status_code}"
    )
