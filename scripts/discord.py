from scripts.settings import version, emscripten
from time import time

if not emscripten:
    from pypresence import Presence


class Discord(object):
    def __init__(self):
        self.client_id = "1125682987552481311"
        self.connected = False
        self.startTime = int(time())

        if not emscripten:
            from nest_asyncio import apply
            apply()
        else:
            print("Discord RPC server not found")

    def prepare(self):
        try:
            self.RPC = Presence(client_id=self.client_id)
            self.RPC.connect()
        except Exception as e:
            print(type(e).__name__, e)
        else:
            print("Discord RPC server found")
            self.connected = True

    def update(self, state: str):
        self.RPC.update(
            state=f"Currently in {state}",  # depending on gamestate
            details=f"Playing on {version}",
            start=self.startTime,
            large_image="icon",
            # join="MTI4NzM0OjFpMmhuZToxMjMxMjM= ",  # use player id in CC
            # party_id="ae488379-351d-4a4f-ad32-2b9b01c91657",  # use game id in CC
            # party_size=[1, 5]
            buttons=[{
                "label": "Play the prototype!",
                "url": "https://richkdev.itch.io/cleanup-catastrophe-proto"
            }]
        )


discord = Discord()
