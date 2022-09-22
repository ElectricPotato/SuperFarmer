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

        #win = 1+6+12+36+72 = 127

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

        elif("smallDog" in theirAnimals and theirAnimals["smallDog"] > 0 and self.herd["smallDog"] > 0):
            failReason = "player already has a small dog"

        elif("bigDog" in theirAnimals and theirAnimals["bigDog"] > 0 and self.herd["bigDog"] > 0):
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
    def __init__(self, idN = None, bankRef = None, gameType = "standard", randomGenerator = random.Random()) -> None:

        self.bankRef = bankRef
        self.idN = idN
        self.gameType = gameType
        self.randomGenerator = randomGenerator

        self.herd = {
            "rabbit" : 0,
            "sheep"  : 0,
            "pig"    : 0,
            "cow"    : 0,
            "horse"  : 0,
            
            "smallDog" : 0,
            "bigDog"   : 0
        }

        if(self.gameType == "dynamic"):
            self.transferFromBank({"rabbit": 1})
    
    def roll(self):
        dieOrange = \
              ["horse"]      \
            + ["fox"]        \
            + ["pig"]    * 2 \
            + ["sheep"]  * 2 \
            + ["rabbit"] * 6

        dieBlue = \
              ["wolf"]       \
            + ["cow"]        \
            + ["pig"]        \
            + ["sheep"]  * 3 \
            + ["rabbit"] * 6

        return [self.randomGenerator.choice(dieOrange), self.randomGenerator.choice(dieBlue)]

    def transferAllToBank(self, animalList):
        def dictFilter(d, names):
            return dict(filter(lambda x: x[0] in names, d.items()))

        self.transferToBank(dictFilter(self.herd, animalList))

    def foxAttack(self):
        if(self.herd["smallDog"]):
            self.transferAllToBank(["smallDog"])
        else:
            self.transferAllToBank(["rabbit"])
            if(self.gameType == "dynamic"):
                self.transferFromBank({"rabbit": 1})
                

    def wolfAttack(self):
        if(self.herd["bigDog"]):
            self.transferAllToBank(["bigDog"])
        else:
            if(self.gameType == "dynamic"):
                self.transferAllToBank(["sheep", "pig", "cow"])
            else:
                self.transferAllToBank(["rabbit", "sheep", "pig", "cow"])

            

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