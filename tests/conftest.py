import quart.flask_patch
import os

from pathlib import Path

import pytest

from flask_caching import Cache
from quart import Quart, render_template

from quart_compress import Compress

_ROOT = Path(".").resolve()


@pytest.fixture
def setup_with_sizes():
    app = Quart(__name__)
    app.testing = True
    Compress(app)

    small_path = _ROOT / "tests" / "templates" / "small.html"
    large_path = _ROOT / "tests" / "templates" / "large.html"

    small_size = os.path.getsize(small_path.as_posix()) - 1
    large_size = os.path.getsize(large_path.as_posix()) - 1

    @app.route("/small")
    def small():
        return render_template("small.html")

    @app.route("/large")
    def large():
        return render_template("large.html")

    return (app, small_size, large_size)


@pytest.fixture
def setup(setup_with_sizes):
    app, _, _ = setup_with_sizes

    return app


@pytest.fixture
def setup_app():
    compress = Compress()
    app = Quart(__name__)
    app.testing = True

    return app, compress


@pytest.fixture
def setup_two_applications():
    compress1 = Compress()
    compress2 = Compress()

    app1 = Quart(__name__)
    app1.testing = True

    app2 = Quart(__name__)
    app2.testing = True

    @app1.route("/small")
    @app2.route("/small")
    def small():
        return render_template("small.html")

    @app1.route("/large")
    @app2.route("/large")
    def large():
        return render_template("large.html")

    return (app1, compress1, app2, compress2)


@pytest.fixture
def setup_with_cache_and_sizes():
    compress = Compress()

    app = Quart(__name__)
    app.testing = True

    cache = Cache(app, config={"CACHE_TYPE": "simple"})
    app.config["COMPRESS_CACHE_BACKEND"] = cache
    app.config["COMPRESS_CACHE_KEY"] = str

    small_path = _ROOT / "tests" / "templates" / "small.html"
    large_path = _ROOT / "tests" / "templates" / "large.html"

    small_size = os.path.getsize(small_path.as_posix()) - 1
    large_size = os.path.getsize(large_path.as_posix()) - 1

    @app.route("/small")
    @cache.cached(timeout=50)
    def small():
        return render_template("small.html")

    @app.route("/large")
    @cache.cached(timeout=50)
    def large():
        return render_template("large.html")

    return (app, compress, small_size, large_size)


@pytest.fixture
def setup_with_cache(setup_with_cache_and_sizes):
    app, compress, _, _ = setup_with_cache_and_sizes

    return app, compress
