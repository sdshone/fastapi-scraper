import requests
from bs4 import BeautifulSoup
from typing import List
from models import ScraperConfig, Product

class Scraper:
    async def scrape(self, settings: ScraperConfig) -> List[Product]:
        products = []
        base_url = settings.url # eg https://dentalstall.com/shop/page
        for page in range(1, settings.pages + 1):
            url = f"{base_url}/{page}/"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            items = soup.find_all("li", class_="product")
            for item in items:
                title = item.find("h2", class_="woo-loop-product__title").text.strip()
                price = float(item.find("span", class_="woocommerce-Price-amount").text.strip().replace('₹', '').replace(',', ''))
                image_url = item.find("img", class_="attachment-woocommerce_thumbnail")["src"]
                product = Product(title=title, price=price, image=image_url)
                products.append(product)

        return products
