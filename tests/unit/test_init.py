from quart_compress import Compress


def test_constructor_init(setup):
    app = setup
    Compress(app)


def test_delayed_init(setup):
    app = setup
    compress = Compress()
    compress.init_app(app)
