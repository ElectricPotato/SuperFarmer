from game_engine import An, Player, GameBank, Herd
from typing import Dict, List, Optional, Tuple, Type

def strategy1_Simple(player: Player, gameBank: GameBank, otherPlayers: List[Player]) -> Optional[Tuple[Type[Herd], Dict, Dict]]:

    #trade format: (otherAgent, yourAnimals, theirAnimals)
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


#once it can win, it will trade animals to fill the missing slots
def strategy2_Simple(player: Player, gameBank: GameBank, otherPlayers: List[Player]) -> Optional[Tuple[Type[Herd], Dict, Dict]]:

    #trade format: (otherAgent, yourAnimals, theirAnimals)
    trades = [
        (lambda : player.herdHasAtLeast({An.cow:    3}), (gameBank, {An.cow:    2}, {An.horse:    1})),
        (lambda : player.herdHasAtLeast({An.cow:    2}), (gameBank, {An.cow:    1}, {An.bigDog:   1})),
        (lambda : player.herdHasAtLeast({An.pig:    4}), (gameBank, {An.pig:    3}, {An.cow:      1})),
        (lambda : player.herdHasAtLeast({An.sheep:  3}), (gameBank, {An.sheep:  2}, {An.pig:      1})),
        (lambda : player.herdHasAtLeast({An.sheep:  2}), (gameBank, {An.sheep:  1}, {An.smallDog: 1})),
        (lambda : player.herdHasAtLeast({An.rabbit: 7}), (gameBank, {An.rabbit: 6}, {An.sheep:    1}))
    ]


    if player.canWin():
        trades = [
            (lambda : player.herd[An.horse] == 0, (gameBank, {An.cow:    2}, {An.horse:    1})),
            (lambda : player.herd[An.horse] == 0, (gameBank, {An.pig:    6}, {An.horse:    1})),
            (lambda : player.herd[An.horse] == 0, (gameBank, {An.sheep: 12}, {An.horse:    1}))
            #TODO: make this trade more than one type of animal for a horse/other missing animals
        ]

        missingAnimals = list(filter(lambda x: player.herd[x] == 0, [An.horse, An.cow, An.pig, An.sheep, An.rabbit]))
        for missingAnimal in missingAnimals:
            pass

    for condition, trade in trades:
        if condition() and player.isTradePossible(*trade):
            return trade

    return None