from quart_compress import Compress


def test_constructor_init(setup_app):
    app, _ = setup_app
    Compress(app)


def test_delayed_init(setup_app):
    app, compress = setup_app
    compress.init_app(app)
