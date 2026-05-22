import os
import pypresence as dc
import asyncio

from time import time
from scripts.common import VERSION


class DiscordRPCManager:
    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        self.loop = loop
        self.client_id: str = "1125682987552481311"
        self.connected: bool = False
        self.startTime = int(time())
        self.RPC = dc.presence.AioPresence(client_id=self.client_id, loop=self.loop)

    async def prepare(self) -> None:
        try:
            await self.RPC.connect()
        except Exception as e:
            print(type(e).__name__, e)
            if e == dc.exceptions.PipeClosed:
                await self.reconnect()
        else:
            print("Discord RPC server found")
            self.connected = True

    async def update(self, state: str) -> None:
        try:
            await self.RPC.update(
                pid=os.getpid(),
                state=state,
                details=VERSION,
                start=self.startTime,
                large_image="icon",
                buttons=[
                    {
                        "label": "Play the prototype!",
                        "url": "https://richkdev.itch.io/cleanup-catastrophe-proto"
                    },
                    {
                        "label": "Check out the source!",
                        "url": "https://github.com/richkdev/Cleanup-Catastrophe"
                    }
                ]
            )
        except Exception as e:
            if e == dc.exceptions.PipeClosed:
                await self.reconnect()
        else:
            print("Discord RPC updated!")
            self.connected = True

    async def reconnect(self) -> None:
        self.connected = False
        del self.RPC
        self.RPC = dc.presence.AioPresence(client_id=self.client_id, loop=self.loop)
        await self.RPC.connect()
        self.connected = True

    async def quit(self) -> None:
        self.connected = False
        await self.RPC.clear()
        self.RPC.close()
