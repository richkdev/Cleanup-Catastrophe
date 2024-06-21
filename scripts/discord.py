from scripts.settings import version, emscripten, FPS
from time import time

if not emscripten:
    try:
        from pypresence import Presence
        from nest_asyncio import apply
        apply()
    except ImportError:
        print("Couldn't import pypresence for Discord RPC.")


class Discord(object):
    def __init__(self):
        self.client_id: str = "1125682987552481311"
        self.connected: bool = False
        self.startTime = int(time())
        self.increment = 0

    def prepare(self):
        try:
            self.RPC = Presence(client_id=self.client_id)
            self.RPC.connect()
        except Exception as e:
            print(type(e).__name__, e)
            pass
        else:
            print("Discord RPC server found")
            self.connected = True

    def update(self, state: str):
        if self.increment % 10 == 0:
            self.RPC.update(
                state=f"Currently in {state}",  # depending on gamestate
                details=f"Playing on {version}",
                start=self.startTime,
                large_image="icon",
                join="MTI4NzM0OjFpMmhuZToxMjMxMjM= ",  # use player id in CC
                party_id="ae488379-351d-4a4f-ad32-2b9b01c91657",  # use game id in CC
                party_size=[1, 5]
                # buttons=[{
                #     "label": "Play the prototype!",
                #     "url": "https://richkdev.itch.io/cleanup-catastrophe-proto"
                # }]
            )
            print("Discord RPC updated!")
        self.increment +=1


discord = Discord()
