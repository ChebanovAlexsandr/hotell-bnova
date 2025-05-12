import allure
import requests
import pytest

HOST = "https://public-api.reservationsteps.ru/v1/api/"

# Получаем данные из БД
# UID = "uid=d7494710-8c8c-4c4c-bba4-f71caf96fece"
# account_id = "535"
NAME = "Отель «Вилла Олива» , API"
ADDRESS = "Санкт-Петербург, Коломяжский пр-кт, 15, к 2"
PHONE = "+799955555"
EMAIL = "alena.s@bnovo.ru"
HOTEL_TYPE = "hotel"


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
    1.2 Получение информации о Категории номеров test_get_roomtypes:
        Проверки:
        * Проверка, что для каждой категории номеров возвращаются: id, name, description;
        * Корректные данные о вместимости: adults, children;
        * Список фотографий (если photos не null);
        * Проверка локализации (name_ru,name_en и т.д.).
        Входные данные:
        * Передали валидный account_id;
        * Передали account_id 0;
        * Передали пустой account_id;
        * Передали несуществующий account_id;
        * Передали неверный формат account_id.
    1.3 Получение информации о Тарифах test_get_plans:
        * Проверка, что тарифы содержат: id, name, description;
        * Проверка на корректные данные о предоплате (booking_guarantee_sum,booking_guarantee_unit);
        * Проверка полей правила отмены (cancellation_rules,cancellation_deadline)   
        Входные данные:
        * Передали валидный account_id;
        * Передали пустой account_id;
        * Передали несуществующий account_id;
        * Передали 0 account_id.
         
          """)
@allure.description("Получение мета-информации об отеле")
@allure.story("Get_accounts")
@pytest.mark.parametrize("uid, status_code", [
    ("uid=d7494710-8c8c-4c4c-bba4-f71caf96fece", 200),
    ("uid=d7494710-8c8c-4c4c-bba4-f71caf96fec", 404),
    ("uid=", 406)
])
def test_get_accounts(uid, status_code):
    request_accounts = requests.get(f"{HOST}accounts?{uid}")
    assert request_accounts.status_code == status_code, f"The status code is not {status_code}"

    """Специальные проверки для Мета-информация об отеле"""
    request = request_accounts.json()

    if status_code == 200:
        with allure.step("Проверка в название отеля"):
            assert request['account']['name'] == NAME, f"Ошибка в название отеля, верное название {NAME}"
        with allure.step("Проверка адреса отеля"):
            assert request['account']['address'] == ADDRESS, f"Ошибка в адресе, верное название {ADDRESS}"
        with allure.step("Проверка номера отеля"):
            assert request['account']['phone'] == PHONE, f"Ошибка в номере, верное название {PHONE}"
        with allure.step("Проверка email отеля"):
            assert request['account']['email'] == EMAIL, f"Ошибка в эл. почте, верное название {EMAIL}"
        with allure.step("Проверка типа отеля"):
            assert request['account']['hotel_type'] == HOTEL_TYPE, f"Ошибка в типе, верное название {HOTEL_TYPE}"


OPTIONAL_FIELDS = ['id', 'name', 'description']
supported_languages = ["ru", "en", "de", "zh", "es", "pl", "fr", "ja", "it", "ko", "fi", "lt"]


@allure.description("Получение информации категории номеров")
@allure.story("Get_roomtypes")
@pytest.mark.parametrize("account_id, status_code", [
    ("535", 200),
    ("0", 200),
    ("", 406),
    ("-1", 404),
    ('"535"', 500)
])
def test_get_roomtypes(account_id, status_code):
    request_roomtypes = requests.get(f"{HOST}roomtypes?account_id={account_id}")
    assert request_roomtypes.status_code == status_code, f"The status code is not {status_code}"

    """Специальные проверки для Категории номеров"""
    request = request_roomtypes.json()

    with allure.step("Проверка, что для каждой категории номеров возвращаются необходимы поля"):
        if status_code == 200:
            if account_id == "0":
                pytest.xfail("Неизвестная ошибка: account_id=0 возвращает пустой список, уточнить требования")
            for room in request["rooms"]:
                with allure.step("Проверка наличия обязательных полей"):
                    for field in OPTIONAL_FIELDS:
                        assert field in room, f"Поле '{field}' отсутствует в категории {room.get('id')}"

                with allure.step("Проверка типов данных"):
                    assert isinstance(room["adults"], int), f"adults должен быть целым числом (категория {room['id']})"
                    assert isinstance(room["children"], int), f"children должно быть целым числом (категория {room['id']})"

                with allure.step("Проверка фотографий"):
                    photos = room.get("photos")
                    if photos is not None:
                        assert isinstance(photos, list), f"Photos должен быть списком (категория {room['id']})"
                        for photo in photos:
                            assert "id" in photo, f"Фото не содержит ID (категория {room['id']})"
                            assert "url" in photo, f"Фото не содержит URL (категория {room['id']})"
                            assert photo["url"].startswith(
                                ("http://", "https://")), f"Некорректный URL (категория {room['id']})"

                with allure.step("Проверка локализации"):
                    for lang in supported_languages:
                        name_field = f"name_{lang}"
                        assert name_field in room, f"Поле {name_field} отсутствует (категория {room['id']})"
                        assert isinstance(room[name_field],
                                          str), f"Поле {name_field} должно быть строкой (категория {room['id']})"


REGULATION_CANCEL = ['id', 'name', 'description', "cancellation_rules", "cancellation_deadline"]


@allure.description("Получение информации о Тарифах")
@allure.story("Get_plans")
@pytest.mark.parametrize("account_id, status_code", [
    ("535", 200),
    ("", 406),
    ("-1", 404),
    ('0', 500)
])
def test_get_plans(account_id, status_code):
    request_plans = requests.get(f"{HOST}plans?account_id={account_id}")
    assert request_plans.status_code == status_code, f"The status code is not {status_code}"

    if status_code == 200:
        """Специальные проверки для Тарифы"""
        request = request_plans.json()

        with allure.step("Проверка, что тарифы содержат необходимые поля"):
            for plans in request["plans"]:
                for field in OPTIONAL_FIELDS:
                    assert field in plans, f"Поле '{field}' отсутствует в категории {plans.get('id')}"

            with allure.step("Проверка типов данных"):
                pytest.xfail("Oшибка: возвращается str вместо float")
                assert isinstance(plans["booking_guarantee_sum"],
                                  float), f"booking_guarantee_sum должен быть float (категория {plans['id']})"
                assert isinstance(plans["booking_guarantee_unit"],
                                  str), f"booking_guarantee_unit должно быть str (категория {plans['id']})"

