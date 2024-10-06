# WIP, use enums

from enum import Enum, auto
from scripts.states.states import *

class States(Enum):
    SPLASH = 1
    LOBBY = auto()
    SCOREBOARD = auto()
    SHOP = auto()
    CATASTROPHE = auto()

game = None # temp

states = {
    States.SPLASH: Splash(game=game),
    States.LOBBY: Lobby(game=game),
    States.SCOREBOARD: Scoreboard(game=game),
    States.SHOP: Shop(game=game),
    States.CATASTROPHE: Catastrophe(game=game),
}
