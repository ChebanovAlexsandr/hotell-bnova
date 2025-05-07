import requests
import pytest

HOST = "https://public-api.reservationsteps.ru/v1/api/"

# Получаем данные из БД
UID = "uid=d7494710-8c8c-4c4c-bba4-f71caf96fece"
account_id = "535"
NAME = "Отель «Вилла Олива» , API"
ADDRESS = "Санкт-Петербург, Коломяжский пр-кт, 15, к 2"
PHONE = "+799955555"
EMAIL = "alena.s@bnovo.ru"
HOTEL_TYPE = "hotel"


@pytest.mark.smoke
@pytest.mark.parametrize("a, b", [
    ("uid=d7494710-8c8c-4c4c-bba4-f71caf96fec", 404),
])
def test_get_accounts(a, b):
    request_accounts = requests.get(f"{HOST}accounts?{a}")
    assert request_accounts.status_code == b, f"The status code is not {b}"

    """Специальные проверки для Мета-информация об отеле"""
    print(request_accounts.json())
    # assert request_accounts.json()['account']['name'] == NAME, f"Ошибка в название отеля, верное название {NAME}"
    # assert request_accounts.json()['account']['address'] == ADDRESS, f"Ошибка в адресе, верное название {ADDRESS}"
    # assert request_accounts.json()['account']['phone'] == PHONE, f"Ошибка в номере, верное название {PHONE}"
    # assert request_accounts.json()['account']['email'] == EMAIL, f"Ошибка в эл. почте, верное название {EMAIL}"
    # assert request_accounts.json()['account'][
    #            'hotel_type'] == HOTEL_TYPE, f"Ошибка в типе, верное название {HOTEL_TYPE}"


test_get_accounts()

OPTIONAL_FIELDS = ['id', 'name', 'description']
supported_languages = ["ru", "en", "de", "zh", "es", "pl", "fr", "ja", "it", "ko", "fi", "lt"]


def get_roomtypes():
    request_roomtypes = requests.get(f"{HOST}roomtypes?account_id={account_id}")
    assert request_roomtypes.status_code == 200, "The status code is not 200"

    """Специальные проверки для Категории номеров"""
    request = request_roomtypes.json()

    """Проверка, что для каждой категории номеров возвращаются"""
    for room in request["rooms"]:
        # Проверка наличия обязательных полей
        for field in OPTIONAL_FIELDS:
            assert field in room, f"Поле '{field}' отсутствует в категории {room.get('id')}"

        # Проверка типов данных
        assert isinstance(room["adults"], int), f"adults должен быть целым числом (категория {room['id']})"
        assert isinstance(room["children"], int), f"children должно быть целым числом (категория {room['id']})"

        # Проверка фотографий
        photos = room.get("photos")
        if photos is not None:
            assert isinstance(photos, list), f"Photos должен быть списком (категория {room['id']})"
            for photo in photos:
                assert "id" in photo, f"Фото не содержит ID (категория {room['id']})"
                assert "url" in photo, f"Фото не содержит URL (категория {room['id']})"
                assert photo["url"].startswith(("http://", "https://")), f"Некорректный URL (категория {room['id']})"

        # Проверка локализации
        for lang in supported_languages:
            # Проверка полей name_{lang}
            name_field = f"name_{lang}"
            assert name_field in room, f"Поле {name_field} отсутствует (категория {room['id']})"
            assert isinstance(room[name_field], str), f"Поле {name_field} должно быть строкой (категория {room['id']})"


get_roomtypes()

REGULATION_CANCEL = ['id', 'name', 'description', "cancellation_rules", "cancellation_deadline"]


def get_plans():
    request_plans = requests.get(f"{HOST}plans?account_id={account_id}")
    assert request_plans.status_code == 200, "The status code is not 200"

    """Специальные проверки для Тарифы"""
    request = request_plans.json()

    # Проверка, что тарифы содержат
    for plans in request["plans"]:
        # Проверка наличия обязательных полей
        for field in OPTIONAL_FIELDS:
            assert field in plans, f"Поле '{field}' отсутствует в категории {plans.get('id')}"

        # Проверка типов данных
        assert isinstance(plans["booking_guarantee_sum"],
                          float), f"booking_guarantee_sum должен быть float (категория {plans['id']})"
        assert isinstance(plans["booking_guarantee_unit"],
                          str), f"booking_guarantee_unit должно быть str (категория {plans['id']})"

    print(request_plans)
    print(request_plans.json())


get_plans()
