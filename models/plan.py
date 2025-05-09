from typing import Union

from pydantic import BaseModel


class Plan(BaseModel):
    id: int
    name: str
    description: Union[str, None]
    booking_guarantee_sum: float
    booking_guarantee_unit: str
    cancellation_rules: str
    cancellation_deadline: int
