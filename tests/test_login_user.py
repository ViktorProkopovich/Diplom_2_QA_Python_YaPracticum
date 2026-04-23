import pytest
import allure
import requests
from helpers.endpoints import Endpoints
from helpers.status_code import StatusCode
from helpers.messages import TextResponse


WORKING_USER = {
    "email": "viktorprokopovich3131@ya.ru",
    "password": "qwerty1234"
}

@allure.feature("Пользователь")
@allure.story("Авторизация")
class TestUserLogin:

    @allure.title("Вход под существующим пользователем")
    def test_login_user(self):
        response = requests.post(Endpoints.LOGIN, json=WORKING_USER)

        assert response.status_code == StatusCode.OK
        assert response.json()["success"] is True
        assert "accessToken" in response.json()

    @allure.title("Вход с неверным логином и паролем")
    def test_login_invalid(self):
        payload = {
            "email": "viktorprokopovich31@ya.ru",
            "password": "qwerty12345"
        }

        response = requests.post(Endpoints.LOGIN, json=payload)

        assert response.status_code == StatusCode.UNAUTHORIZED
        assert response.json()["message"] == TextResponse.INCORRECT_CREDENTIALS
        