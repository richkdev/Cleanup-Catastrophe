#!/usr/bin/env python

from os import chdir, path
chdir(path.dirname(path.abspath(__file__)))

import asyncio

if __name__ == "__main__":
    from scripts.game import Game
    asyncio.run(Game().main())
