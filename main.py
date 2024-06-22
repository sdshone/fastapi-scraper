from typing import List
from fastapi import FastAPI
from models import ScraperConfig, Product
from scraper import  Scraper
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, world!"}

@app.post("/scrape")
async def scrape(settings: ScraperConfig):
    scraper = Scraper()
    products: List[Product] = await scraper.scrape(settings=settings)
    return {"scraped_products": len(products)}
