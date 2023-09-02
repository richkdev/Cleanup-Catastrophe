# turn into a seperate thread, which tries to connect every few seconds

from pypresence import Presence
from time import time


def checkRPC():
    t = int(time())

    try:
        RPC = Presence("1125682987552481311")

        RPC.connect()

        RPC.update(
            state="Clean the ocean by fishing out all that nasty trash!",
            details="v.ALPHA.1.0.0",
            large_image="game",
            buttons=[{
                "label": "Download",
                "url": "https://richkdev.itch.io/cleanup-catastrophe"
            }],
            start=t
        )

        print("Discord RPC: ACTIVATED")

    except Exception as e:
        print("Discord RPC:", e)
        pass
