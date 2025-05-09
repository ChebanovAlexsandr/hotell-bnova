import requests
from config.settings import settings


class APIClient:
    def __init__(self):
        self.base_url = settings.HOST
        self.requests = requests

    def get_accounts(self, uid: str):
        return self.requests.get(f"{self.base_url}accounts?{uid}")

    def get_roomtypes(self, account_id: str):
        return self.requests.get(f"{self.base_url}roomtypes?account_id={account_id}")

    def get_plans(self, account_id: str):
        return self.requests.get(f"{self.base_url}plans?account_id={account_id}")
