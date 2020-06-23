import base64
import io

import aiohttp

from zaneapi.errors import *
from zaneapi.enums import Operation

BASE = "http://127.0.0.1:5000/api/"


def _requires_session(func):
    async def wrapper(self, *args, **kwargs):
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return await func(self, *args, **kwargs)
    return wrapper


class HTTP:

    def __init__(self, session: aiohttp.ClientSession = None):
        self._session = session

    @staticmethod
    async def _get_response_content(response):
        try:
            return await response.json()
        except aiohttp.ContentTypeError:
            return await response.read()

    @staticmethod
    def _base64_encode_bytes_io(bytes_io: io.BytesIO) -> str:
        value = bytes_io.getvalue()
        encoded = base64.b64encode(value)
        return encoded.decode("ascii")

    @staticmethod
    def _base64_decode_string(to_decode: str) -> bytes:
        return base64.b64decode(to_decode)

    @_requires_session
    async def post(self, url, json):
        async with self._session.post(url, json=json) as response:
            return await self._get_response_content(response)

    @_requires_session
    async def get(self, url):
        async with self._session.get(url) as response:
            return await self._get_response_content(response)

    async def manipulate(self, operation: Operation, image_bytes: io.BytesIO):
        json = dict(image=self._base64_encode_bytes_io(image_bytes))
        response_content = await self.post(BASE + operation.value, json=json)

        if response_content.get("status", 400) == 400:
            raise BadRequest(response_content.get("message"))

        image_raw = response_content.get("image")
        image = io.BytesIO(self._base64_decode_string(image_raw))
        image.seek(0)

        return image
