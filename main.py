from typing import List
from fastapi import FastAPI, Depends
from models import ScraperConfig, Product
from scraper import  Scraper
from notifier import ConsoleNotifier
from storage import JSONStorage
from auth import authenticate


app = FastAPI()
scraper = Scraper(storage=JSONStorage(), notifier=ConsoleNotifier())

@app.get("/")
async def root():
    return {"message": "Hello, world!"}

@app.post("/scrape", dependencies=[Depends(authenticate)])
async def scrape(settings: ScraperConfig):
    products: List[Product] = await scraper.scrape(settings=settings)
    return {"scraped_products": len(products)}
