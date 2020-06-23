import io


class Asset:

    def __init__(self, client, bytes_io=None, url=None):
        self.bytes = bytes_io
        self.url = url

        self._http = client.http

    async def read(self):
        if self.bytes is None:
            return io.BytesIO(await self._http.get(self.url))
        return self.bytes
