from pydantic import BaseModel
from typing import Optional, List

class Place(BaseModel):
    name: str
    address: str
    phone: Optional[str] = None
    type: Optional[str] = None
    rating: Optional[float] = None
    description: Optional[str] = None

class SearchRequest(BaseModel):
    city: str
    area: str
    type: str

class SearchResponse(BaseModel):
    success: bool
    query: str
    places: List[Place]
    count: int