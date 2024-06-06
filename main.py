#!/usr/bin/env python

import asyncio
from os import chdir, path
chdir(path.dirname(path.abspath(__file__)))


if __name__ == "__main__":
    from scripts.game import Game
    asyncio.run(Game().main())
