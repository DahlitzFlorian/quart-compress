import os

from pathlib import Path

import pytest

from quart import Quart, render_template
from quart_compress import Compress


_ROOT = Path(".").resolve()


@pytest.fixture
def setup_with_sizes():
    app = Quart(__name__)
    app.testing = True

    small_path = _ROOT / "tests" / "templates" / "small.html"
    large_path = _ROOT / "tests" / "templates" / "large.html"

    small_size = os.path.getsize(small_path.as_posix()) - 1
    large_size = os.path.getsize(large_path.as_posix()) - 1

    Compress(app)

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
