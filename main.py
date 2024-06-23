from typing import List
from fastapi import FastAPI, Depends, Body
from models import ScraperConfig, Product
from scraper import  Scraper
from notifier import ConsoleNotifier
from storage import JSONStorage
from auth import authenticate
from cache import RedisCache


app = FastAPI()
scraper = Scraper(storage=JSONStorage(), notifier=ConsoleNotifier(), cache=RedisCache())

@app.get("/")
async def root():
    return {"message": "Hello, world!"}

@app.post("/scrape", dependencies=[Depends(authenticate)])
async def scrape(
    pages: int = Body(default=1, embed=True),
    proxy: str = Body(default=None, embed=True)
):
    config = ScraperConfig(pages=pages, proxy=proxy)
    result: List[Product] = await scraper.scrape(config)
    return {"scraped_products": len(result)}