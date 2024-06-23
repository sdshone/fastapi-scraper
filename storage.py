import json
from models import Product
from abc import ABC, abstractmethod
import os

class Storage(ABC):
    """
    Abstract base class for a storage system.
    """
    @abstractmethod
    def save(self, data: Product):
        """
        Save the given product data.
        """
        raise NotImplementedError

class JSONStorage(Storage):
    """
    JSON-based storage implementation.
    """
    def __init__(self, file_path: str = "scraped_data.json"):
        """
        Initialize the JSONStorage with a file path.
        """
        self.file_path = file_path

        # Check if the file exists and delete it if it does before the scraper runs
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
            print(f"Deleted existing file: {self.file_path}")

    def save(self, data: Product):
        """
        Save the product data to a JSON file.
        """
        try:
            with open(self.file_path, "r") as f:
                scraped_data = json.load(f)
        except FileNotFoundError:
            scraped_data = []
        scraped_data.append(data.model_dump_json())
        with open(self.file_path, "w") as f:
            json.dump(scraped_data, f, indent=4)
        print('Product saved to JSON successfully.')
