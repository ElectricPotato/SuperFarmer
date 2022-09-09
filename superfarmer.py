'''
notes:
in a standard game, if fox and wolf is rolled symultaniously, both dogs are used up even though the wolf already took the rabbits, so the small dog gets taken away while it has nothing to protect

'''

'''
#old version of breedPairs
def breedPairs(self, roll): 
    herd_from_die = {animal: roll.count(animal) for animal in animals_list}
    temporary_total_herd = {animal: herd_from_die[animal] + self.herd[animal] for animal in animals_list}
    offspring = {animal: temporary_total_herd[animal]//2 for animal in animals_list}
    new_total_herd = {animal: self.herd[animal] + offspring[animal] for animal in animals_list}
'''


import random
from typing import Dict, List, Optional, Tuple

from datetime import datetime

animals_list = [
    "rabbit",
    "sheep",
    "pig",
    "cow",
    "horse"
]


die_orange = \
      ["horse"]      \
    + ["fox"]        \
    + ["pig"]    * 2 \
    + ["sheep"]  * 2 \
    + ["rabbit"] * 6

die_blue = \
      ["wolf"]       \
    + ["cow"]        \
    + ["pig"]        \
    + ["sheep"]  * 3 \
    + ["rabbit"] * 6

#players: 2 - 4

N_PLAYERS = 1

GAME_TYPE = "standard" # or "dynamic"

def dict_filter(d, names):
    return dict(filter(lambda x: x[0] in names, d.items()))

#example: self.transferToBank(dict_filter(self.herd, ["smallDog"]))

#TODO: break this out to seperate files
class GameState():
    def __init__(self, type = "player", idN = None, bankRef = None) -> None:
        self.type = type

        if(type == "player"):
            self.bankRef = bankRef

            self.idN = idN

            self.herd = {
                "rabbit" : 0,
                "sheep"  : 0,
                "pig"    : 0,
                "cow"    : 0,
                "horse"  : 0,
                
                "smallDog" : 0,
                "bigDog"   : 0
            }

            if(GAME_TYPE == "dynamic"):
                self.transferFromBank({"rabbit": 1})

        elif(type == "bank"):
            self.herd = {
                "rabbit" : 60,
                "sheep"  : 24,
                "pig"    : 20,
                "cow"    : 12,
                "horse"  :  4,

                "smallDog" : 4,
                "bigDog"   : 2
            }
    
    def roll():
        return [random.choice(die_orange), random.choice(die_blue)]

    def foxAttack(self): #todo: transfer to bank
        if(self.herd["smallDog"]):
            self.transferToBank({"smallDog": self.herd["smallDog"]})
        else:
            if(GAME_TYPE == "dynamic"):
                self.transferToBank({"rabbit": max(self.herd["rabbit"] -1, 0) })
            else:
                self.herd["rabbit"] = 0
                self.transferToBank({"rabbit": self.herd["rabbit"]})

    def wolfAttack(self): #todo: transfer to bank
        if(self.herd["bigDog"]):
            self.transferToBank({"bigDog": self.herd["bigDog"]})
        else:
            if(GAME_TYPE == "dynamic"):
                self.transferToBank(dict_filter(self.herd, ["sheep", "pig", "cow"]))
            else:
                self.transferToBank(dict_filter(self.herd, ["rabbit", "sheep", "pig", "cow"]))

            

    def breedPairs(self, roll):
        uniqueAnimals = list(set(roll))
        offspring = {animal: (self.herd[animal] + roll.count(animal))//2 for animal in uniqueAnimals}
        self.transferFromBank(offspring)

    def executeRoll(self, roll):
        attack = False
        if("wolf" in roll):
            self.wolfAttack()
            attack = True
        if("fox" in roll):
            self.foxAttack()
            attack = True
        
        if(not attack):
            self.breedPairs(roll)

        return roll
            

    def herdToTradePoints(herd):
        # trade points
        # rabbit = 1
        # sheep = 6
        # pig = 12
        # cow = 36
        # horse = 72

        # smallDog = 6
        # bigDog = 36

        #win = 1+6+12+36+72

        tradePoints = {}
        tradePoints["rabbit"] = 1
        tradePoints["sheep"]  = tradePoints["rabbit"] * 6
        tradePoints["pig"]    = tradePoints["sheep"]  * 2
        tradePoints["cow"]    = tradePoints["pig"]    * 3
        tradePoints["horse"]  = tradePoints["cow"]    * 2

        tradePoints["smallDog"] = tradePoints["sheep"]
        tradePoints["bigDog"]   = tradePoints["cow"]

        total = sum(herd[animal] * tradePoints[animal] for animal in herd)

        return total

    def tradePoints(self):
        return GameState.herdToTradePoints(self.herd)
        
    def herdHasAtLeast(self, animals):
        return all(self.herd[animal] >= n for animal, n in animals.items())
    
    def isTradePossible(self, otherAgent, yourAnimals, theirAnimals, printReason = False, acceptUnfairTrade = False):
        tradeSuccess = False
        failReason = ""

        if(self.type == "bank"):
            failReason = "bank cant trade" #TODO: make bank a different class

        elif not (len(yourAnimals) > 0 and len(theirAnimals) > 0):
            failReason = "no animals traded"

        elif not (len(yourAnimals) == 1 or len(theirAnimals) == 1):
            failReason = "at least one side of the trade has to have only 1 animal"

        elif not (GameState.herdToTradePoints(yourAnimals) == GameState.herdToTradePoints(theirAnimals)):
            failReason = "trade value not equal"

        elif not (self.herdHasAtLeast(yourAnimals)):
            failReason = "you dont have enough animals"

        elif(not acceptUnfairTrade and not otherAgent.herdHasAtLeast(theirAnimals)):
            failReason = "other side doesnt have enough animals"

        elif("smallDog" in theirAnimals and theirAnimals["smallDog"] and self.herd["smallDog"] > 0):
            failReason = "player already has a small dog"

        elif("bigDog" in theirAnimals and theirAnimals["bigDog"] and self.herd["bigDog"] > 0):
            failReason = "player already has a big dog"

        else:
            tradeSuccess = True

        if not tradeSuccess:
            if printReason:
                print(self, otherAgent, yourAnimals, theirAnimals)
                print(failReason)

        return tradeSuccess

    def trade(self, otherAgent, yourAnimals, theirAnimals):
        if self.isTradePossible(otherAgent, yourAnimals, theirAnimals, printReason = True, acceptUnfairTrade = True):
            self.transfer(otherAgent, yourAnimals)
            otherAgent.transfer(self, theirAnimals)

    def transfer(fromAgent, toAgent, transferHerd):
        for animal, n in transferHerd.items():
            available = fromAgent.herd[animal]
            transferAmount = min(available, n)

            fromAgent.herd[animal] -= transferAmount
            toAgent.herd[animal] += transferAmount

    def transferToBank(self, transferHerd):
        self.transfer(self.bankRef, transferHerd)

    def transferFromBank(self, transferHerd):
        self.bankRef.transfer(self, transferHerd)

    def hasWon(self) -> bool:
        return self.herd["rabbit"] \
           and self.herd["sheep"]  \
           and self.herd["pig"]    \
           and self.herd["cow"]    \
           and self.herd["horse"]

    def canWin(self) -> bool:
        winningHerd = {
            "rabbit" : 1,
            "sheep"  : 1,
            "pig"    : 1,
            "cow"    : 1,
            "horse"  : 1,
        }
        
        return self.tradePoints() >= GameState.herdToTradePoints(winningHerd)


def strategy1_Simple(player: GameState, gameBank: GameState, otherPlayers: List[GameState]) -> Optional[Tuple[GameState, Dict, Dict]]:
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
    gameBank = GameState(type = "bank")
    players = [
        GameState(
            type = "player",
            idN = i,
            bankRef = gameBank
        )
        for i in range(N_PLAYERS)
    ]

    Rseed = int(datetime.now().timestamp()*1000000)
    random.seed(Rseed)

    print(f"seed {Rseed}")


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

            roll = GameState.roll()
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
