# /usr/bin/env python

from os import chdir, path
chdir(path.dirname(path.abspath(__file__)))

if __name__ == "__main__":
    from threading import Thread

    from scripts.discordRPC import discordRPC
    from scripts.game import game

    discord = Thread(target=discordRPC)
    game = Thread(target=game)

    discord.start()
    game.start()

    discord.join()
    game.join()
