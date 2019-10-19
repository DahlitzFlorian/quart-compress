from quart.wrappers import Response


class ResponseWrapper(Response):
    def __init__(self, *args, **kwargs):
        self.direct_passthrough = False
        super().__init__(self, *args, **kwargs)
