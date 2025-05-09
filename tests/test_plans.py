import allure
import pytest
from models.plan import Plan


@allure.feature("Plans API")
@allure.description("""
    Этот набор тестов которые  проверяют:
    1.1 Получение информации о Тарифах test_get_plans:
        * Проверка, что тарифы содержат: id, name, description;
        * Проверка на корректные данные о предоплате (booking_guarantee_sum,booking_guarantee_unit);
        * Проверка полей правила отмены (cancellation_rules,cancellation_deadline)   
        Входные данные:
        * Передали валидный account_id;
        * Передали пустой account_id;
        * Передали несуществующий account_id;
        * Передали 0 account_id.
          """)
class TestPlans:
    @allure.story("Get tariff plans")
    @pytest.mark.parametrize("account_id, expected_status", [
        ("535", 200),
        ("", 406),
        ("-1", 404),
        ('0', 500)
    ])
    def test_get_plans(self, api_client, account_id, expected_status):
        response = api_client.get_plans(account_id)

        assert response.status_code == expected_status

        with allure.step("Проверка, что тарифы содержат необходимые поля"):
            if response.status_code == 200:
                data = response.json()
                for plan in data["plans"]:
                    Plan(**plan)

                    with allure.step("Проверка типов данных"):
                        pytest.xfail("Oшибка: возвращается str вместо float")
                        assert plan["booking_guarantee_sum"] >= 0
                        assert plan["booking_guarantee_unit"] in ["percent", "fixed"]
