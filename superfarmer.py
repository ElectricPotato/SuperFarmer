'''
notes:
in a standard game, if fox and wolf is rolled symultaniously, both dogs are used up even though the wolf already took the rabbits, so the small dog gets taken away while it has nothing to protect

'''
from game_engine import *

import random
from typing import Dict, List, Optional, Tuple, Type

from datetime import datetime

#players: 2 - 4
N_PLAYERS = 1

GAME_TYPE = GameType.standard



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

    #this strategy breaks if fox eats everything: {'rabbit': 0, 'sheep': 24, 'pig': 20, 'cow': 12, 'horse': 4, 'smallDog': 1, 'bigDog': 1}

def runGame():
    gameRunning = True

    randSeed = int(datetime.now().timestamp()*1000000)
    randomGenerator = random.Random()
    randomGenerator.seed(randSeed)
    print(f"seed {randSeed}")

    gameBank = GameBank()
    players = [
        Player(
            idN = i,
            bankRef = gameBank,
            gameType = GAME_TYPE,
            randomGenerator = randomGenerator
        )
        for i in range(N_PLAYERS)
    ]



    gameRound = 1
    while(gameRunning):
        gameRunning = True
        for i, player in enumerate(players):
            if(player.hasWon()):
                continue

            print(player.herd, f"{player.tradePoints()}/127")

            #gameRunning = True

            #trade before roll
            #single trade destination, single animal to be exchanged for multiple or vice versa, not multiple for multiple
            #you are allowed to trade dogs back and forth

            otherPlayers = list(filter(lambda x: x is not player, players))
            #TODO: store which strategy the player is using inside GameState class 
            currentTrade = strategy1_Simple(player, gameBank, otherPlayers)
            if currentTrade is not None:
                player.trade(*currentTrade)

                if(player.hasWon()):
                    print(f"player {i} has won in round {gameRound}")
                    print(player.herd, f"{player.tradePoints()}/127")
                    gameRunning = False
                    continue

            roll = player.roll()
            #roll = ["rabbit", "rabbit"]
            player.executeRoll(roll)
            print(f"trade {currentTrade}")
            print(f"roll {roll}")
            

            if(player.hasWon()):
                print(f"player {i} has won in round {gameRound}")
                print(player.herd, f"{player.tradePoints()}/127")
                gameRunning = False
                continue

            if(player.canWin()):
                print(f"player {i} can win next turn")
                print(player.herd, f"{player.tradePoints()}/127")

        gameRound += 1
        print()

        if(gameRound > 400):
            print(gameBank.herd)
            break

    return gameRound

while(1):
    if(runGame() >= 390):
        print("this run seems to have broken somehow")
        break
