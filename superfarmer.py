'''
notes:
in a standard game, if fox and wolf is rolled symultaniously, both dogs are used up even though the wolf already took the rabbits, so the small dog gets taken away while it has nothing to protect

'''

import random
from typing import Dict, List, Optional, Tuple, Union

from datetime import datetime

#players: 2 - 4
N_PLAYERS = 1

GAME_TYPE = "standard" # or "dynamic"

#TODO: break this out to seperate files

from game_engine import *


TradePartner = Union[GameBank, Player]

def strategy1_Simple(player: Player, gameBank: GameBank, otherPlayers: List[Player]) -> Optional[Tuple[TradePartner, Dict, Dict]]:
    tradeDestination = gameBank

    #def tryTradeAndLeaveOne(tradeYourAnimals, tradeTheirAnimals):

    #trades = 

    if(player.herdHasAtLeast({"cow":    3}) and gameBank.herdHasAtLeast({"horse":    1})):
        tradeYourAnimals, tradeTheirAnimals = {"cow":    2}, {"horse":    1}

    elif(player.herdHasAtLeast({"cow":    2}) and gameBank.herdHasAtLeast({"bigDog":   1}) and player.herd["bigDog"] == 0):
        tradeYourAnimals, tradeTheirAnimals = {"cow":    1}, {"bigDog":   1}

    elif(player.herdHasAtLeast({"pig":    4}) and gameBank.herdHasAtLeast({"cow":      1})):
        tradeYourAnimals, tradeTheirAnimals = {"pig":    3}, {"cow":      1}

    elif(player.herdHasAtLeast({"sheep":  3}) and gameBank.herdHasAtLeast({"pig":      1})):
        tradeYourAnimals, tradeTheirAnimals = {"sheep":  2}, {"pig":      1}

    elif(player.herdHasAtLeast({"sheep":  2}) and gameBank.herdHasAtLeast({"smallDog": 1}) and player.herd["smallDog"] == 0):
        tradeYourAnimals, tradeTheirAnimals = {"sheep":  1}, {"smallDog": 1}

    elif(player.herdHasAtLeast({"rabbit": 7}) and gameBank.herdHasAtLeast({"sheep":    1})):
        tradeYourAnimals, tradeTheirAnimals = {"rabbit": 6}, {"sheep":    1}

    else:
        return None

    return (tradeDestination, tradeYourAnimals, tradeTheirAnimals)

    #this strategy breaks if fox eats everything: {'rabbit': 0, 'sheep': 24, 'pig': 20, 'cow': 12, 'horse': 4, 'smallDog': 1, 'bigDog': 1}

def runGame():
    gameRunning = True

    Rseed = int(datetime.now().timestamp()*1000000)
    random_generator = random.Random()
    random_generator.seed(Rseed)
    print(f"seed {Rseed}")

    gameBank = GameBank()
    players = [
        Player(
            idN = i,
            bankRef = gameBank,
            random_generator = random_generator
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

        if(gameRound > 400): break

    return gameRound

while(1):
    if(runGame() >= 390):
        print("this run seems to have broken somehow")
        break
