import pytest
import allure
import requests
from faker import Faker
from helpers.endpoints import Endpoints
from helpers.status_code import StatusCode
from helpers.messages import TextResponse

fake = Faker('en_US')

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
    def test_create_existing_user(self):
        user_data = {"email": fake.email(),
                     "password": fake.password(length=10, special_chars=False, digits=True, upper_case=False),
                     "name": fake.first_name()}
        
        response1 = requests.post(Endpoints.REGISTER, json=user_data)
        assert response1.status_code == StatusCode.OK

        response2 = requests.post(Endpoints.REGISTER, json=user_data)
        assert response2.status_code == StatusCode.FORBIDDEN

        assert response2.json()["message"] == TextResponse.USER_ALREADY_EXISTS

        token = response1.json()["accessToken"]
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
