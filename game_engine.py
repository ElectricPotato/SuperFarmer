import random

class Herd():
    def __init__(self) -> None:
        self.herd = {}

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
        return Herd.herdToTradePoints(self.herd)
        
    def herdHasAtLeast(self, animals):
        return all(self.herd[animal] >= n for animal, n in animals.items())
    
    def isTradePossible(self, otherAgent, yourAnimals, theirAnimals, printReason = False, acceptUnfairTrade = False):
        tradeSuccess = False
        failReason = ""

        if not (len(yourAnimals) > 0 and len(theirAnimals) > 0):
            failReason = "no animals traded"

        elif not (len(yourAnimals) == 1 or len(theirAnimals) == 1):
            failReason = "at least one side of the trade has to have only 1 animal"

        elif not (Herd.herdToTradePoints(yourAnimals) == Herd.herdToTradePoints(theirAnimals)):
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

class Player(Herd):
    def __init__(self, idN = None, bankRef = None, game_type = "standard", random_generator = random.Random()) -> None:

        self.bankRef = bankRef

        self.idN = idN

        self.game_type = game_type

        self.random_generator = random_generator

        self.herd = {
            "rabbit" : 0,
            "sheep"  : 0,
            "pig"    : 0,
            "cow"    : 0,
            "horse"  : 0,
            
            "smallDog" : 0,
            "bigDog"   : 0
        }

        if(self.game_type == "dynamic"):
            self.transferFromBank({"rabbit": 1})
    
    def roll(self):
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

        return [self.random_generator.choice(die_orange), self.random_generator.choice(die_blue)]

    def foxAttack(self): #todo: transfer to bank
        if(self.herd["smallDog"]):
            self.transferToBank({"smallDog": self.herd["smallDog"]})
        else:
            if(self.game_type == "dynamic"):
                self.transferToBank({"rabbit": max(self.herd["rabbit"] -1, 0) })
            else:
                self.herd["rabbit"] = 0
                self.transferToBank({"rabbit": self.herd["rabbit"]})

    def wolfAttack(self): #todo: transfer to bank
        def dict_filter(d, names):
            return dict(filter(lambda x: x[0] in names, d.items()))

        if(self.herd["bigDog"]):
            self.transferToBank({"bigDog": self.herd["bigDog"]})
        else:
            if(self.game_type == "dynamic"):
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
        
        return self.tradePoints() >= Herd.herdToTradePoints(winningHerd)

    def transferToBank(self, transferHerd):
        self.transfer(self.bankRef, transferHerd)

    def transferFromBank(self, transferHerd):
        self.bankRef.transfer(self, transferHerd)


class GameBank(Herd):
    def __init__(self) -> None:
        self.herd = {
            "rabbit" : 60,
            "sheep"  : 24,
            "pig"    : 20,
            "cow"    : 12,
            "horse"  :  4,

            "smallDog" : 4,
            "bigDog"   : 2
        }