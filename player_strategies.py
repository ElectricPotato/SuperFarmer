from game_engine import *
from typing import Dict, List, Optional, Tuple, Type

def strategy1_Simple(player: Player, gameBank: GameBank, otherPlayers: List[Player]) -> Optional[Tuple[Type[Herd], Dict, Dict]]:

    trades = [
        (lambda : player.herdHasAtLeast({An.cow:    3}), (gameBank, {An.cow:    2}, {An.horse:    1})),
        (lambda : player.herdHasAtLeast({An.cow:    2}), (gameBank, {An.cow:    1}, {An.bigDog:   1})),
        (lambda : player.herdHasAtLeast({An.pig:    4}), (gameBank, {An.pig:    3}, {An.cow:      1})),
        (lambda : player.herdHasAtLeast({An.sheep:  3}), (gameBank, {An.sheep:  2}, {An.pig:      1})),
        (lambda : player.herdHasAtLeast({An.sheep:  2}), (gameBank, {An.sheep:  1}, {An.smallDog: 1})),
        (lambda : player.herdHasAtLeast({An.rabbit: 7}), (gameBank, {An.rabbit: 6}, {An.sheep:    1}))
    ]

    for condition, trade in trades:
        if condition() and player.isTradePossible(*trade):
            return trade

    return None