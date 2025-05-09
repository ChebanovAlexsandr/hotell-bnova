from pydantic import BaseModel
from typing import List, Optional, Union


class Photo(BaseModel):
    id: int
    url: str


class RoomType(BaseModel):
    id: int
    name: str
    description: Union[str, None]
    adults: int
    children: int
    photos: Optional[List[Photo]] = None
    name_ru: str
    name_en: str
