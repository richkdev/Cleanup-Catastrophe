from scripts.globals import version, emscripten
from time import time

if not emscripten:
    from pypresence import AioPresence

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
            details=version,
            start=self.startTime,
            large_image="icon",
            # join="MTI4NzM0OjFpMmhuZToxMjMxMjM= ",
            # party_id="ae488379-351d-4a4f-ad32-2b9b01c91657",
            # party_size=[1, 5]
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
