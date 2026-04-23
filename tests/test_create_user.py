import pytest
import allure
import requests
from faker import Faker
from helpers.endpoints import Endpoints
from helpers.status_code import StatusCode
from helpers.messages import TextResponse

fake = Faker('en_US')

WORKING_USER = {"email": f"{fake.user_name()}.{fake.random_number(digits=6)}@ya.ru",
                "password": "qwerty1234",
                "name": fake.first_name()}

resp = requests.post(Endpoints.REGISTER, json=WORKING_USER)


class TestUserCreation:

    @allure.title("Создать уникального пользователя")
    def test_create_unique_user(self):
        user_data = {"email": fake.email(),
                     "password": fake.password(length=10, special_chars=False, digits=True, upper_case=False),
                     "name": fake.first_name()}
        response = requests.post(Endpoints.REGISTER, json=user_data)

        assert response.status_code == StatusCode.OK
        assert response.json()["success"] is True
        assert "accessToken" in response.json()

        access_token = response.json()["accessToken"]
        requests.delete(Endpoints.USER, headers={"Authorization": f"Bearer {access_token}"})

    @allure.title("Создать пользователя, который уже зарегистрирован")
    def test_create_working_user(self):
        response = requests.post(Endpoints.REGISTER, json=WORKING_USER)

        assert response.status_code == StatusCode.FORBIDDEN
        assert response.json()["message"] == TextResponse.USER_ALREADY_EXISTS

        login_resp = requests.post(Endpoints.LOGIN, json={
            "email": WORKING_USER["email"],
            "password": WORKING_USER["password"]})
        if login_resp.status_code == StatusCode.OK:
            token = login_resp.json()["accessToken"]
            requests.delete(Endpoints.USER, headers={"Authorization": f"Bearer {token}"})

    @allure.title("Создать пользователя и не заполнить одно из обязательных полей")
    @pytest.mark.parametrize("required_field", ["email", "password", "name"])
    def test_create_user_missing_required_field(self, required_field):
        user_data = {"email": fake.email(),
                     "password": fake.password(length=10, special_chars=False, digits=True, upper_case=False),
                     "name": fake.first_name()}
        del user_data[required_field]

        response = requests.post(Endpoints.REGISTER, json=user_data)

        assert response.status_code == StatusCode.FORBIDDEN
        assert response.json()["message"] == TextResponse.REQUIRED_FIELDS
