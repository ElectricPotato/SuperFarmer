import random

from enum import Enum, auto

class An(Enum): #animal
    rabbit   = auto()
    sheep    = auto()
    pig      = auto()
    cow      = auto()
    horse    = auto()

    smallDog = auto()
    bigDog   = auto()

    fox      = auto() #not used in herds
    wolf     = auto()

    def __str__(self):
        return {
            An.rabbit   :'R',
            An.sheep    :'S',
            An.pig      :'P',
            An.cow      :'C',
            An.horse    :'H',

            An.smallDog :'d',
            An.bigDog   :'D',

            An.fox      :'f',
            An.wolf     :'w',
        }[self]

    def __repr__(self) -> str: #this is not the best solution, but its easy
        return self.__str__()

    def longName(self):
        return {
            An.rabbit   :'Rabbit',
            An.sheep    :'Sheep',
            An.pig      :'Pig',
            An.cow      :'Cow',
            An.horse    :'Horse',

            An.smallDog :'Small Dog',
            An.bigDog   :'Big Dog',
            
            An.fox      :'Fox',
            An.wolf     :'Wolf',
        }[self]



class GameType(Enum):
    standard = auto()
    dynamic  = auto()


class Herd():
    def __init__(self, herd = {}) -> None:
        self.herd = herd


    def herdToStr(self):
        return ', '.join(f"{animal} {self.herd[animal]}" for animal in [An.rabbit, An.sheep, An.pig, An.cow, An.horse, An.smallDog, An.bigDog])

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
        tradePoints[An.rabbit]   = 1
        tradePoints[An.sheep]    = tradePoints[An.rabbit] * 6
        tradePoints[An.pig]      = tradePoints[An.sheep]  * 2
        tradePoints[An.cow]      = tradePoints[An.pig]    * 3
        tradePoints[An.horse]    = tradePoints[An.cow]    * 2
        tradePoints[An.smallDog] = tradePoints[An.sheep]
        tradePoints[An.bigDog]   = tradePoints[An.cow]

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

        elif(An.smallDog in theirAnimals and theirAnimals[An.smallDog] > 0 and self.herd[An.smallDog] > 0):
            failReason = "player already has a small dog"

        elif(An.bigDog in theirAnimals and theirAnimals[An.bigDog] > 0 and self.herd[An.bigDog] > 0):
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
    def __init__(self, herd = None, idN = None, bankRef = None, gameType = GameType.standard, randomGenerator = random.Random()) -> None:

        self.bankRef = bankRef
        self.idN = idN
        self.gameType = gameType
        self.randomGenerator = randomGenerator

        if(herd is None):
            self.herd = {
                An.rabbit : 0,
                An.sheep  : 0,
                An.pig    : 0,
                An.cow    : 0,
                An.horse  : 0,
                
                An.smallDog : 0,
                An.bigDog   : 0
            }
        else:
            self.herd = herd

        if(self.gameType == GameType.dynamic):
            self.transferFromBank({An.rabbit: 1})

    def __str__(self) -> str:
        return f"player {i}"

    def herdToStr(self):
        return super().herdToStr() + f", {self.tradePoints()}/127"
    
    def roll(self):
        dieOrange = \
              [An.horse]      \
            + [An.fox]        \
            + [An.pig]    * 2 \
            + [An.sheep]  * 2 \
            + [An.rabbit] * 6

        dieBlue = \
              [An.wolf]       \
            + [An.cow]        \
            + [An.pig]        \
            + [An.sheep]  * 3 \
            + [An.rabbit] * 6

        return [self.randomGenerator.choice(dieOrange), self.randomGenerator.choice(dieBlue)]

    def transferAllToBank(self, animalList):
        def dictFilter(d, names):
            return dict(filter(lambda x: x[0] in names, d.items()))

        self.transferToBank(dictFilter(self.herd, animalList))

    def foxAttack(self):
        if(self.herd[An.smallDog]):
            self.transferAllToBank([An.smallDog])
        else:
            self.transferAllToBank([An.rabbit])
            if(self.gameType == GameType.dynamic):
                self.transferFromBank({An.rabbit: 1})
                

    def wolfAttack(self):
        if(self.herd[An.bigDog]):
            self.transferAllToBank([An.bigDog])
        else:
            if(self.gameType == GameType.dynamic):
                self.transferAllToBank([An.sheep, An.pig, An.cow])
            else:
                self.transferAllToBank([An.rabbit, An.sheep, An.pig, An.cow])

            

    def breedPairs(self, roll):
        uniqueAnimals = list(set(roll))
        offspring = {animal: (self.herd[animal] + roll.count(animal))//2 for animal in uniqueAnimals}
        self.transferFromBank(offspring)

    def executeRoll(self, roll):
        attack = False
        if(An.wolf in roll):
            self.wolfAttack()
            attack = True
        if(An.fox in roll):
            self.foxAttack()
            attack = True
        
        if(not attack):
            self.breedPairs(roll)

    def hasWon(self) -> bool:
        return self.herd[An.rabbit] \
           and self.herd[An.sheep]  \
           and self.herd[An.pig]    \
           and self.herd[An.cow]    \
           and self.herd[An.horse]

    def canWin(self) -> bool:
        winningHerd = {
            An.rabbit : 1,
            An.sheep  : 1,
            An.pig    : 1,
            An.cow    : 1,
            An.horse  : 1,
        }
        
        return self.tradePoints() >= Herd.herdToTradePoints(winningHerd)

    def transferToBank(self, transferHerd):
        self.transfer(self.bankRef, transferHerd)

    def transferFromBank(self, transferHerd):
        self.bankRef.transfer(self, transferHerd)


class GameBank(Herd):
    def __init__(self, herd = None) -> None:
        if(herd is None):
            self.herd = {
                An.rabbit : 60,
                An.sheep  : 24,
                An.pig    : 20,
                An.cow    : 12,
                An.horse  :  4,

                An.smallDog : 4,
                An.bigDog   : 2
            }
        else:
            self.herd = herd

    def __str__(self) -> str:
        return "bank"