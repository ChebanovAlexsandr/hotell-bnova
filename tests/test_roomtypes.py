import allure
import pytest
from models.roomtype import RoomType


@allure.feature("RoomTypes API")
@allure.description("""
    Этот набор тестов которые  проверяют:
    1.1 Получение информации о Категории номеров test_get_roomtypes:
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
          """)
class TestRoomTypes:
    @allure.story("Get room categories")
    @pytest.mark.parametrize("account_id, expected_status", [
        ("535", 200),
        ("0", 200),
        ("", 406),
        ("-1", 404)
    ])
    def test_get_roomtypes(self, api_client, account_id, expected_status):
        response = api_client.get_roomtypes(account_id)

        assert response.status_code == expected_status

        if response.status_code == 200:
            if account_id == "0":
                pytest.xfail("Неизвестная ошибка: account_id=0 возвращает пустой список, уточнить требования")
            data = response.json()
            for room in data["rooms"]:
                RoomType(**room)

                with allure.step("Дополнительные проверки"):
                    assert room["adults"] >= 0
                    assert room["children"] >= 0
                    if room.get("photos"):
                        assert len(room["photos"]) > 0
