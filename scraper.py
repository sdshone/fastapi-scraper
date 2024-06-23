import asyncio
import time
import requests
from bs4 import BeautifulSoup
from typing import List, Optional
from models import ScraperConfig, Product
from storage import Storage
from notifier import Notifier
from cache import Cache
import os

class Scraper:
    def __init__(self, storage: Storage, notifier: Notifier, cache: Cache):
        """
        Initialize the Scraper with storage, notifier, and cache strategies
        """
        self.storage = storage
        self.notifier = notifier
        self.cache = cache

    async def scrape(self, config: ScraperConfig) -> List[Product]:
        """
        Scrape products from the specified config (ScraperConfig): 
        The configuration for scraping including number of pages and proxy.
        Stores the products based on storage strategy and if the product is not cached already
        Returns the list of ALL scraped products.
        """
        products = []
        base_url = 'https://dentalstall.com/shop/page'
        for page in range(1, config.pages + 1):
            url = f"{base_url}/{page}/"

            response = await self._make_request(url, config.proxy)
            soup = BeautifulSoup(response.content, "html.parser")

            items = soup.find_all("li", class_="product")
            for item in items:
                title = item.find("h2", class_="woo-loop-product__title").text.strip()
                price = float(item.find("span", class_="woocommerce-Price-amount").text.strip().replace('₹', '').replace(',', ''))
                image_url = item.find("img", class_="attachment-woocommerce_thumbnail")["data-lazy-src"]
                
                # Using the product link as the cache key as title is can be same for different products
                # Not added product_url as part of the Product as the requirement does not mention it
                product_url = item.find("a", class_="buy-now-btn")["href"]

                image_path = self._download_image(image_url)
                product = Product(title=title, price=price, image=image_path)
                products.append(product)

                # We want to save to storage and update cache only if currently not cached/ price now updated.
                if not await self.cache.is_cached(product, product_url) or await self.cache.is_price_changed(product, product_url):
                    self.storage.save(product)
                    await self.cache.update_cache(product, product_url)

        self.notifier.notify(f"Scraped {len(products)} products")
        return products

    async def _make_request(self, url: str, proxy: Optional[str]) -> requests.Response:
        """
        Make an HTTP GET request to the specified URL with optional proxy support and returns response.
        """
        retries = 3
        while retries > 0:
            try:
                if proxy:
                    response = requests.get(url, proxies={"http": proxy, "https": proxy})
                else:
                    response = requests.get(url)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                retries -= 1
                if retries == 0:
                    raise e
                await asyncio.sleep(2) # simple backoff - can be exponential
        raise requests.RequestException('Request failed')

    def _download_image(self, url: str) -> str:
        """
        Download an image from the specified URL and save it locally.
        Returns the local file path of the downloaded image.
        """
        response = requests.get(url)
        if not os.path.exists("images"):
            os.makedirs("images")

        file_name = os.path.join("images", os.path.basename(url))

        with open(file_name, "wb") as f:
            f.write(response.content)

        return file_name