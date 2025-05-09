import allure
import pytest
from config.settings import settings
from models.account import AccountResponse


@allure.feature("Accounts API")
@allure.description("""
    Этот набор тестов которые  проверяют:
    1.1. Получение мета-информации об отеле test_get_accounts:
        Проверки:
        * Проверка, что возвращаются корректные данные отеля (название, адрес, контакты);
        * Проверка поля hotel_type (должен содержать допустимые значения: hotel,apartments и т.д.).
        Входные данные:
        * Корректный uid;
        * Некорректный uid; 
        * Пустой uid.
        """)
class TestAccounts:
    @allure.story("Get hotel metadata")
    @pytest.mark.parametrize("uid, expected_status", [
        (settings.VALID_UID, 200),
        (settings.INVALID_UID, 404),
        ("", 406)
    ])
    def test_get_accounts(self, api_client, uid, expected_status):
        with allure.step(f"Send request with uid: {uid}"):
            response = api_client.get_accounts(uid)

        with allure.step("Check status code"):
            assert response.status_code == expected_status

        if response.status_code == 200:
            with allure.step("Validate response structure"):
                AccountResponse(**response.json()["account"])

            with allure.step("Check content values"):
                account_data = response.json()["account"]
                assert account_data["name"] == settings.NAME, f"Ошибка в название отеля, верное название {settings.NAME}"
                assert account_data['address'] == settings.ADDRESS,  f"Ошибка в адресе, верное название {settings.ADDRESS}"
                assert account_data['phone'] == settings.PHONE, f"Ошибка в номере, верное название {settings.PHONE}"
                assert account_data['email'] == settings.EMAIL, f"Ошибка в эл. почте, верное название {settings.EMAIL}"
                assert account_data["hotel_type"] in settings.HOTEL_TYPE, f"Ошибка в типе hotel_type"
