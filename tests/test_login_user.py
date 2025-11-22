import pytest
import allure
import requests
from faker import Faker
from helpers.endpoints import Endpoints
from helpers.status_code import StatusCode
from helpers.messages import TextResponse

fake = Faker('en_US')

class TestUserLogin:

    @allure.title("Вход под существующим пользователем")
    def test_login_user(self):
        user_data = {"email": fake.unique.email(),
                     "password": fake.password(length=10, special_chars=False, digits=True, upper_case=False),
                     "name": fake.first_name()}
    
        register_resp = requests.post(Endpoints.REGISTER, json=user_data)
        assert register_resp.status_code == StatusCode.OK

        login_resp = requests.post(Endpoints.LOGIN, json={"email": user_data["email"],
                                                          "password": user_data["password"]})
 
        assert login_resp.status_code == StatusCode.OK
        assert login_resp.json()["success"] is True
        assert "accessToken" in login_resp.json()

        token = login_resp.json()["accessToken"]
        requests.delete(Endpoints.USER, headers={"Authorization": f"Bearer {token}"})

    @allure.title("Вход с неверным логином и паролем")
    def test_login_invalid(self):
        
        payload = {"email": fake.email(),
                   "password": fake.password(length=10, special_chars=False, digits=True, upper_case=False)}

        response = requests.post(Endpoints.LOGIN, json=payload)

        assert response.status_code == StatusCode.UNAUTHORIZED
        assert response.json()["message"] == TextResponse.INCORRECT_CREDENTIALS
