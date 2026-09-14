import asyncio

class BaseManager:
    """
    Bare bones manager class, don't use directly!
    """

    def __init__(self) -> None:
        raise NotImplementedError

    def update(self) -> None:
        raise NotImplementedError

    def quit(self) -> None:
        raise NotImplementedError


class LoopManager(BaseManager):
    """
    Bare bones manager class for things that use the event loop, don't use directly!
    """

    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        self.loop = loop
