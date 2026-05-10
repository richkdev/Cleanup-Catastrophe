import os
import pypresence as dc

from time import time
from scripts.common import VERSION


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
                await self.reconnect()
        else:
            print("Discord RPC server found")
            self.connected = True

    async def update(self, state: str) -> None:
        try:
            await self.RPC.update(
                pid=os.getpid(),
                activity_type=dc.types.ActivityType.PLAYING,
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
        self.RPC = dc.presence.AioPresence(client_id=self.client_id)
        await self.RPC.connect()

    async def quit(self) -> None:
        self.connected = False
        self.RPC.close()
