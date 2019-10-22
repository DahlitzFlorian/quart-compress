""" Quart Compress: Compresses your quart responses """
import asyncio

from gzip import GzipFile
from io import BytesIO
from typing import Union, AnyStr

from quart import request, current_app, Quart
from quart.local import LocalProxy

from .typing import ResponseWrapper as Response


class DictCache:
    def __init__(self):
        self.data = {}

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value


class Compress:
    """
    The Compress object is the entry point for your application.
    When initialising a Compress object you may optionally provide your
    :class:`quart.Quart` application object if it is ready. Otherwise,
    you may provide it later by using the :meth:`init_app` method.
    :param app: optional :class:`quart.Quart` application object
    :type app: :class:`quart.Quart` or None
    """

    def __init__(self, app: Quart = None) -> None:
        """
        An alternative way to pass your :class:`quart.Quart` application
        object to Quart-Compress. :meth:`init_app` also takes care of some
        default `settings`_.
        :param app: the :class:`quart.Quart` application object.
        """
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Quart) -> None:
        defaults = [
            (
                "COMPRESS_MIMETYPES",
                [
                    "text/html",
                    "text/css",
                    "text/xml",
                    "application/json",
                    "application/javascript",
                ],
            ),
            ("COMPRESS_LEVEL", 6),
            ("COMPRESS_MIN_SIZE", 500),
            ("COMPRESS_CACHE_KEY", None),
            ("COMPRESS_CACHE_BACKEND", None),
            ("COMPRESS_REGISTER", True),
        ]

        for k, v in defaults:
            app.config.setdefault(k, v)

        backend = app.config["COMPRESS_CACHE_BACKEND"]
        self.cache = backend if backend else None
        self.cache_key = app.config["COMPRESS_CACHE_KEY"]

        if app.config["COMPRESS_REGISTER"] and app.config["COMPRESS_MIMETYPES"]:
            app.after_request(self.after_request)

    async def after_request(self, response: Response) -> Response:
        app = self.app or current_app
        accept_encoding = request.headers.get("Accept-Encoding", "")

        if (
            response.mimetype not in app.config["COMPRESS_MIMETYPES"]
            or "gzip" not in accept_encoding.lower()
            or not 200 <= response.status_code < 300
            or (
                response.content_length is not None
                and response.content_length < app.config["COMPRESS_MIN_SIZE"]
            )
            or "Content-Encoding" in response.headers
        ):
            return response

        response.direct_passthrough = False

        if self.cache:
            key = self.cache_key(response)
            gzip_content = self.cache.get(key) or await self.compress(app, response)
            self.cache.set(key, gzip_content)
        else:
            gzip_content = await self.compress(app, response)

        response.set_data(gzip_content)  # type: ignore

        response.headers["Content-Encoding"] = "gzip"
        response.headers["Content-Length"] = response.content_length

        vary = response.headers.get("Vary")
        if vary:
            if "accept-encoding" not in vary.lower():
                response.headers["Vary"] = "{}, Accept-Encoding".format(vary)
        else:
            response.headers["Vary"] = "Accept-Encoding"

        return response

    async def compress(
        self, app: Union[Quart, LocalProxy], response: Response
    ) -> bytes:
        gzip_buffer = BytesIO()

        if asyncio.iscoroutine(response.get_data()):
            data = await response.get_data()
        else:
            data = str(response.get_data())  # pragma: no cover

        with GzipFile(
            mode="wb", compresslevel=app.config["COMPRESS_LEVEL"], fileobj=gzip_buffer
        ) as gzip_file:
            gzip_file.write(data)  # type: ignore

        return gzip_buffer.getvalue()
