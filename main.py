from typing import List
from fastapi import FastAPI, Depends, Body
from models import ScraperConfig, Product
from scraper import Scraper
from notifier import ConsoleNotifier
from storage import JSONStorage
from auth import authenticate
from cache import RedisCache

# Initialize FastAPI app instance
app = FastAPI()

# Initialize Scraper instance with required storage, notification and cache strategies
scraper = Scraper(storage=JSONStorage(), notifier=ConsoleNotifier(), cache=RedisCache())

# Endpoint to initiate scraping process
@app.post("/scrape", dependencies=[Depends(authenticate)])
async def scrape(
    pages: int = Body(default=1, embed=True),  # Default number of pages to scrape
    proxy: str = Body(default=None, embed=True)  # Optional proxy to use for scraping
):
    """
    Endpoint to start scraping products from a website.

    Args:
        pages (int): Number of pages to scrape (default is 1).
        proxy (str, optional): Proxy URL to use for scraping requests.

    Returns JSON response indicating the number of products scraped.
    """
    # Create ScraperConfig object based on request parameters
    config = ScraperConfig(pages=pages, proxy=proxy)
    
    # Call scraper instance to perform scraping with the given configuration
    result: List[Product] = await scraper.scrape(config)

    return {"scraped_products": len(result)}
