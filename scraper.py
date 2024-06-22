import time
import requests
from bs4 import BeautifulSoup
from typing import List
from models import ScraperConfig, Product
import os

class Scraper:
    async def scrape(self, settings: ScraperConfig) -> List[Product]:
        products = []
        base_url = settings.url # eg https://dentalstall.com/shop/page
        for page in range(1, settings.pages + 1):
            url = f"{base_url}/{page}/"
            response = self._make_request(url)
            soup = BeautifulSoup(response.content, "html.parser")
            items = soup.find_all("li", class_="product")
            for item in items:
                title = item.find("h2", class_="woo-loop-product__title").text.strip()
                price = float(item.find("span", class_="woocommerce-Price-amount").text.strip().replace('₹', '').replace(',', ''))
                
                image_url = item.find("img", class_="attachment-woocommerce_thumbnail")["data-lazy-src"]
                image_path = self._download_image(image_url)
                product = Product(title=title, price=price, image=image_path)
                products.append(product)

        return products

    def _make_request(self, url: str) -> requests.Response:
        retries = 3
        while retries > 0:
            try:
                response = requests.get(url)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                retries -= 1
                if retries == 0:
                    raise e
                time.sleep(2) # simple backoff - can be exponential
        raise Exception('Request failed')

    def _download_image(self, url: str) -> str:
        response = requests.get(url)
        if not os.path.exists("images"):
            os.makedirs("images")
        file_name = os.path.join("images", os.path.basename(url))
        with open(file_name, "wb") as f:
            f.write(response.content)
        return file_name
