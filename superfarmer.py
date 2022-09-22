'''
notes:
in a standard game, if fox and wolf is rolled symultaniously, both dogs are used up even though the wolf already took the rabbits, so the small dog gets taken away while it has nothing to protect

'''
from game_engine import *
from player_strategies import *

from typing import Dict, List, Optional, Tuple, Type

from datetime import datetime

#players: 2 - 4
N_PLAYERS = 1

GAME_TYPE = GameType.standard





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

for i in range(100):
    if(runGame() >= 390):
        print("this run seems to have broken somehow")
        break
