from pydantic import BaseModel, HttpUrl

class ScraperConfig(BaseModel):
    url: HttpUrl
    pages: int


class Product(BaseModel):
    title: str
    price: float
    image: str
