import os
import pypresence as dc

from time import time
from scripts.globals import VERSION


class DiscordPresence:
    def __init__(self) -> None:
        self.client_id: str = "1125682987552481311"
        self.connected: bool = False
        self.startTime = int(time())
        self.RPC = dc.presence.AioPresence(client_id=self.client_id)

    async def prepare(self) -> None:
        try:
            await self.RPC.connect()
        except Exception as e:
            print(type(e).__name__, e)
            if e == dc.exceptions.PipeClosed:
                await self.RPC.connect()
        else:
            print("Discord RPC server found")
            self.connected = True

    async def update(self, state: str) -> None:
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
        print("Discord RPC updated!")

    async def quit(self) -> None:
        await self.RPC.clear(os.getpid())
