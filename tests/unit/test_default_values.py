def test_mimetypes_default(setup):
    """ Tests COMPRESS_MIMETYPES default value is set correctly. """
    app = setup

    defaults = [
        "text/html",
        "text/css",
        "text/xml",
        "application/json",
        "application/javascript",
    ]

    assert app.config["COMPRESS_MIMETYPES"] == defaults


def test_level_default(setup):
    """ Tests COMPRESS_LEVEL default value is correctly set. """
    app = setup

    assert app.config["COMPRESS_LEVEL"] == 6


def test_min_size_default(setup):
    """ Tests COMPRESS_MIN_SIZE default value is correctly set. """
    app = setup

    assert app.config["COMPRESS_MIN_SIZE"] == 500
