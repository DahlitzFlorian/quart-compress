import pytest

from integration.helper import _client_get


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@pytest.mark.asyncio
async def test_compress_level(setup_two_applications):
    """ Tests COMPRESS_LEVEL correctly affects response data. """
    app1, compress1, app2, compress2 = setup_two_applications
    app1.config["COMPRESS_LEVEL"] = 1

    compress1.init_app(app1)

    response = await _client_get(app1, "/large")
    data = await response.get_data()
    response1_size = len(data)

    app2.config["COMPRESS_LEVEL"] = 6

    compress2.init_app(app2)

    response = await _client_get(app2, "/large")
    data = await response.get_data()
    response6_size = len(data)

    assert response1_size != response6_size


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@pytest.mark.asyncio
async def test_compress_min_size(setup_with_sizes):
    """ Tests COMPRESS_MIN_SIZE correctly affects response data. """
    app, small_size, large_size = setup_with_sizes
    response = await _client_get(app, "/small")
    data = await response.get_data()
    assert small_size == len(data)

    response = await _client_get(app, "/large")
    data = await response.get_data()
    assert large_size != len(data)


@pytest.mark.asyncio
async def test_mimetype_mismatch(setup):
    """ Tests if mimetype not in COMPRESS_MIMETYPES. """
    app = setup

    response = await _client_get(app, "/static/1.png")
    assert response.mimetype == "image/png"


@pytest.mark.asyncio
async def test_content_length_options(setup):
    app = setup

    client = app.test_client()
    headers = [("Accept-Encoding", "gzip")]
    response = await client.options("/small", headers=headers)

    assert response.status_code == 200
