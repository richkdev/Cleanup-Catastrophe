from time import time, sleep
from sys import platform


def discordRPC():
    connected = False
    t = time()
    delay = 2

    if platform != 'emscripten':
        try:
            from pypresence import Presence
        except ImportError:
            return

        while connected != True:
            try:
                RPC = Presence("1125682987552481311")
                RPC.connect()
                RPC.update(
                    state="Clean the ocean by fishing out all that nasty trash!",
                    details=open("VERSION").read(),
                    large_image="game",
                    buttons=[{
                        "label": "Play the demo!",
                        "url": "https://richkdev.itch.io/cleanup-catastrophe-demo"
                    }],
                    start=int(t)
                )
            except Exception as e:
                print(type(e).__name__)
                if RuntimeError:
                    break
            else:
                print("Discord RPC found")
                connected = True
                break

            delay += 5
            sleep(delay)
    else:
        print("Discord RPC not found")
