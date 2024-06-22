import aioredis
from models import Product

class Cache:
    async def is_cached(self, product: Product) -> bool:
        raise NotImplementedError

    async def is_price_changed(self, product: Product) -> bool:
        raise NotImplementedError

    async def update_cache(self, product: Product):
        raise NotImplementedError

class RedisCache(Cache):
    def __init__(self, redis_url: str = "redis://localhost"):
        self.redis = aioredis.from_url(redis_url)

    async def is_cached(self, product: Product) -> bool:
        cached_product = await self.redis.get(product.title)
        return cached_product is not None

    async def is_price_changed(self, product: Product) -> bool:
        cached_product = await self.redis.get(product.title)
        if cached_product:
            cached_product = Product.model_validate_json(cached_product)
            return cached_product.price != product.price
        return False

    async def update_cache(self, product: Product):
        await self.redis.set(product.title, product.model_dump_json())
