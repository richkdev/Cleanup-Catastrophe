from scripts.globals import VERSION
from time import time

from pypresence.presence import AioPresence

class DiscordPresence:
    def __init__(self) -> None:
        self.client_id: str = "1125682987552481311"
        self.connected: bool = False
        self.startTime = int(time())
        self.RPC = AioPresence(client_id=self.client_id)

    async def prepare(self) -> None:
        try:
            await self.RPC.connect()
        except Exception as e:
            print(type(e).__name__, e)
        else:
            print("Discord RPC server found")
            self.connected = True

    async def update(self, state: str) -> None:
        await self.RPC.update(
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

    def quit(self) -> None:
        self.RPC.close()
