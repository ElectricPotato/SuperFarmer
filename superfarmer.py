'''
notes:
in a standard game, if fox and wolf is rolled symultaniously, both dogs are used up even though the wolf already took the rabbits, so the small dog gets taken away while it has nothing to protect

trade before roll
single trade destination, single animal to be exchanged for multiple or vice versa, not multiple for multiple
you are allowed to trade dogs back and forth
'''
from game_engine import *
import player_strategies as ps

from typing import Dict, List, Optional, Tuple, Type
from datetime import datetime
import random

#players: 2 - 4



def newRandom():
    randSeed = int(datetime.now().timestamp()*1000000)
    randomGenerator = random.Random()
    randomGenerator.seed(randSeed)

    return randomGenerator, randSeed

def runGame(gameType, playerStrategies, maxRounds):
    gameRunning = True

    randomGenerator, randSeed = newRandom()
    print(f"seed {randSeed}")

    nPlayers = len(playerStrategies)

    gameBank = GameBank()
    players = [
        Player(
            idN = i,
            bankRef = gameBank,
            gameType = gameType,
            randomGenerator = randomGenerator
        )
        for i in range(nPlayers)
    ]

    results = [-1] * nPlayers # the number of rounds each player won in, -1 means maxRounds exceeded

    for gameRound in range(maxRounds):
        gameRunning = False
        print(f"--- Round {gameRound} ---")
        for i, player, playerStrategy in zip(range(nPlayers), players, playerStrategies):
            if(player.hasWon()):
                continue

            print(f"player {i}: {player.herdToStr()}")

            otherPlayers = list(filter(lambda x: x is not player, players))
            currentTrade = playerStrategy(player, gameBank, otherPlayers)
            if currentTrade is not None:
                player.trade(*currentTrade)

                if(player.hasWon()):
                    print(f"player {i} has won in round {gameRound}: {player.herdToStr()}")
                    results[i] = gameRound
                    continue

            roll = player.roll()
            #roll = ["rabbit", "rabbit"]
            player.executeRoll(roll)

            if(currentTrade is not None):
                otherAgent, yourAnimals, theirAnimals = currentTrade
                print(f"player {i} trades {yourAnimals} for {otherAgent}'s {theirAnimals}")
            print(f"player {i} rolls {roll[0]} {roll[1]}")

            if(player.hasWon()):
                print(f"player {i} has won in round {gameRound}: {player.herdToStr()}")
                continue
            if(player.canWin()):
                print(f"player {i} can win next turn: {player.herdToStr()}")

            gameRunning = True

        if(not gameRunning):
            break

    print("--- Game End ---")
    return results

print("legend:")
print('\n'.join(f' {animal.__str__()}: {animal.longName()}' for animal in An))
print()

for i in range(1):
    gameType = GameType.standard
    playerStrategies = [ps.strategy1_Simple]
    maxRounds = 400

    print(f"gameType: {gameType.name}, Players: {','.join(map(lambda x: x.__name__, playerStrategies))}, maxRounds: {maxRounds}")
    results = runGame(gameType, playerStrategies, maxRounds)
    print(results)

