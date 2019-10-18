import unittest
import os

from quart import Quart, render_template

from quart_compress import Compress


class DefaultsTest(unittest.TestCase):
    def setUp(self):
        self.app = Quart(__name__)
        self.app.testing = True

        Compress(self.app)

    def test_mimetypes_default(self):
        """ Tests COMPRESS_MIMETYPES default value is set correctly. """
        defaults = [
            "text/html",
            "text/css",
            "text/xml",
            "application/json",
            "application/javascript",
        ]
        self.assertEqual(self.app.config["COMPRESS_MIMETYPES"], defaults)

    def test_level_default(self):
        """ Tests COMPRESS_LEVEL default value is correctly set. """
        self.assertEqual(self.app.config["COMPRESS_LEVEL"], 6)

    def test_min_size_default(self):
        """ Tests COMPRESS_MIN_SIZE default value is correctly set. """
        self.assertEqual(self.app.config["COMPRESS_MIN_SIZE"], 500)


if __name__ == "__main__":
    unittest.main()
