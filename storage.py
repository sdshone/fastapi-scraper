import json
from models import Product
from typing import List

class Storage:
    def save(self, data: Product):
        raise NotImplementedError

class JSONStorage(Storage):
    def __init__(self, file_path: str = "scraped_data.json"):
        self.file_path = file_path

    def save(self, data: Product):
        try:
            with open(self.file_path, "r") as f:
                scraped_data = json.load(f)
        except FileNotFoundError:
            scraped_data = []
        scraped_data.append(data.model_dump_json())
        with open(self.file_path, "w") as f:
            json.dump(scraped_data, f, indent=4)
        print('Product saved to JSON successfully.')
