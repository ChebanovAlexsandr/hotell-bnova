# API Testing Framework

Фреймворк для автоматизации тестирования API отельной системы. Проект включает тесты для:
- Аккаунтов 🏨
- Категорий номеров 🛏️
- Тарифов 💰

## 📦 Структура проекта

project/
├── config/ # Конфигурационные файлы
│ └── settings.py # Настройки окружения
├── tests/ # Тестовые сценарии
│ ├── test_accounts.py # Тесты аккаунтов
│ ├── test_roomtypes.py# Тесты категорий номеров
│ └── test_plans.py # Тесты тарифов
├── utils/ # Вспомогательные модули
│ └── api_client.py # Клиент для работы с API
└── models/ # Модели данных Pydantic
├── account.py # Модель аккаунта
├── roomtype.py # Модель категории номеров
└── plan.py # Модель тарифа


Запуск отчетов allure 
pytest --alluredir=allure_results
allure serve allure_results

## Добавлен github actions с просмотром отчетов Allure на вкадке Actions