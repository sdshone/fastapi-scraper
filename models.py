from pydantic import BaseModel
from typing import Optional

class ScraperConfig(BaseModel):
    pages: Optional[int] = 1  # Default to 1 page if not provided
    proxy: Optional[str] = None  # Default to None if not provided


class Product(BaseModel):
    title: str
    price: float
    image: str
