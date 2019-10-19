import pytest

from quart_compress.quart_compress import DictCache
from integration.helper import _client_get


@pytest.mark.asyncio()
async def test_caching_methods(setup):
    app = setup
    app.config["COMPRESS_CACHE_BACKEND"] = DictCache()
    app.config["COMPRESS_CACHE_BACKEND"].set("cache", "Ipsum Lorem")
    app.config["COMPRESS_CACHE_KEY"] = "cache"

    cache_data = app.config["COMPRESS_CACHE_BACKEND"].get("cache")

    assert cache_data == "Ipsum Lorem"


@pytest.mark.asyncio()
async def test_caching_basic(setup_with_sizes):
    app, small_size, large_size = setup_with_sizes
    app.config["COMPRESS_CACHE_BACKEND"] = DictCache()
    app.config["COMPRESS_CACHE_BACKEND"].set("cache", "Ipsum Lorem")
    app.config["COMPRESS_CACHE_KEY"] = "cache"

    response = await _client_get(app, "/small")
    data = await response.get_data()

    assert small_size == len(data)
