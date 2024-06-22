from typing import List
from fastapi import FastAPI
from models import ScraperConfig, Product
from scraper import  Scraper
from storage import JSONStorage

app = FastAPI()
scraper = Scraper(storage=JSONStorage())

@app.get("/")
async def root():
    return {"message": "Hello, world!"}


@app.post("/scrape")
async def scrape(settings: ScraperConfig):
    products: List[Product] = await scraper.scrape(settings=settings)
    return {"scraped_products": len(products)}
