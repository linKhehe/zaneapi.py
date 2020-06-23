import asyncio
import io
import typing

import aiohttp

from zaneapi.asset import Asset
from zaneapi.enums import Operation
from zaneapi.http import HTTP


class Client:

    def __init__(self, session: aiohttp.ClientSession = None, loop=None):
        self.http = HTTP(session)
        self._loop = loop or asyncio.get_event_loop()

    async def manipulate(self, operation: Operation, image: typing.Union[str, io.BytesIO]):
        if isinstance(image, Asset):
            asset = image
        elif isinstance(image, io.BytesIO):
            asset = Asset(self, bytes_io=image)
        else:
            asset = Asset(self, url=image)

        return await self.http.manipulate(operation, await asset.read())

    async def close(self):
        await self.http._session.close()
