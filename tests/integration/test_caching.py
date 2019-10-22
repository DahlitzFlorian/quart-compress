import pytest

from quart_compress.quart_compress import DictCache
from integration.helper import _client_get


@pytest.mark.asyncio()
async def test_caching_methods(setup_with_cache):
    app, compress = setup_with_cache
    app.config["COMPRESS_CACHE_BACKEND"] = DictCache()
    app.config["COMPRESS_CACHE_BACKEND"].set("cache", "Ipsum Lorem")
    app.config["COMPRESS_CACHE_KEY"] = "cache"

    compress.init_app(app)

    cache_data = app.config["COMPRESS_CACHE_BACKEND"].get("cache")

    assert cache_data == "Ipsum Lorem"


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@pytest.mark.asyncio()
async def test_caching_basic(setup_with_cache_and_sizes):
    app, compress, small_size, large_size = setup_with_cache_and_sizes
    app.config["COMPRESS_CACHE_BACKEND"] = DictCache()
    app.config["COMPRESS_CACHE_BACKEND"].set("cache", "Ipsum Lorem")
    app.config["COMPRESS_CACHE_KEY"] = str

    compress.init_app(app)

    response = await _client_get(app, "/large")
    data = await response.get_data()
    response = await _client_get(app, "/large")
    data = await response.get_data()

    assert large_size != len(data)
