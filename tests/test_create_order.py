import pytest
import allure
import requests
from helpers.endpoints import Endpoints
from helpers.status_code import StatusCode
from helpers.messages import TextResponse

WORKING_USER = {"email": "viktorprokopovich3131@ya.ru",
                "password": "qwerty1234"}

def get_auth_token():
    resp = requests.post(Endpoints.LOGIN, json=WORKING_USER)
    assert resp.status_code == 200, f"Login failed: {resp.text}"
    token = resp.json()["accessToken"]
    return token

class TestOrderCreation:

    @allure.title("Создать заказ с авторизацией и ингредиентами")
    def test_create_order_authorized_with_ingredients(self):
        token = get_auth_token()
        ing_resp = requests.get(Endpoints.GET_INGREDIENTS)
        ingredients = [ing["_id"] for ing in ing_resp.json()["data"][:2]]
        order_resp = requests.post(
            Endpoints.CREATE_ORDER,
            headers={"Authorization": token},
            json={"ingredients": ingredients})
        
        assert order_resp.status_code == 200
        assert order_resp.json()["success"] is True

    @allure.title("Создать заказ без авторизации")
    def test_create_order_unauthorized(self):
        ing_resp = requests.get(Endpoints.GET_INGREDIENTS)
        ingredients = [ing["_id"] for ing in ing_resp.json()["data"][:1]]
        order_resp = requests.post(Endpoints.CREATE_ORDER, json={"ingredients": ingredients})

        assert order_resp.status_code == 200
        assert order_resp.json()["success"] is True

    @allure.title("Создать заказ без ингредиентов")
    def test_create_order_no_ingredients(self):
        token = get_auth_token()
        order_resp = requests.post(
            Endpoints.CREATE_ORDER,
            headers={"Authorization": token},
            json={"ingredients": []})
        
        assert order_resp.status_code == 400
        assert order_resp.json()["message"] == TextResponse.NO_INGREDIENT_IDENTIFIERS

    @allure.title("Создать заказ с неверным хешем ингредиентов")
    def test_create_order_invalid_ingredient_hash(self):
        token = get_auth_token()
        order_resp = requests.post(
            Endpoints.CREATE_ORDER,
            headers={"Authorization": token},
            json={"ingredients": ["invalid_hash_12345"]})
        
        assert order_resp.status_code == 500
