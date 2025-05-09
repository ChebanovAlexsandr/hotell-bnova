from pydantic import BaseModel


class AccountResponse(BaseModel):
    id: int
    name: str
    address: str
    phone: str
    email: str
    hotel_type: str
