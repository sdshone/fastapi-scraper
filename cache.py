import aioredis
from models import Product
from abc import ABC, abstractmethod

class Cache(ABC):
    """
    Abstract base class for a cache strategy.
    """
    @abstractmethod
    async def is_cached(self, product: Product) -> bool:
        """
        Check if the product is cached.
        """
        raise NotImplementedError

    @abstractmethod
    async def is_price_changed(self, product: Product) -> bool:
        """
        Check if the product's price has changed compared to the cached version.
        """
        raise NotImplementedError

    @abstractmethod
    async def update_cache(self, product: Product):
        """
        Update the cache with the given product details.
        """
        raise NotImplementedError

class RedisCache(Cache):
    """
    Redis-based cache implementation.
    """
    def __init__(self, redis_url: str = "redis://localhost"):
        self.redis = aioredis.from_url(redis_url)

    async def is_cached(self, product: Product) -> bool:
        """
        Check if the product is cached.
        """
        cached_product = await self.redis.get(product.title)
        return cached_product is not None

    async def is_price_changed(self, product: Product) -> bool:
        """
        Check if the product's price has changed compared to the cached version.
        """
        cached_product = await self.redis.get(product.title)
        if cached_product:
            cached_product = Product.model_validate_json(cached_product)
            return cached_product.price != product.price
        return False

    async def update_cache(self, product: Product):
        """
        Update the cache with the given product details.
        """
        await self.redis.set(product.title, product.model_dump_json())
        print('Product cache created/updated to Redis successfully.')
