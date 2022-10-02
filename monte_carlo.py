# Roulette Game 
import random
import matplotlib.pyplot as plt

class FairRoulette():
    def __init__(self):
        self.pockets = [] 
        for i in range(1, 37): # you can bet number from 1-36
            self.pockets.append(i)
        self.ball = None
        self.pocketOdds = len(self.pockets) - 1 # if you bet $1 and win, you get $36 back. ($35+$1)
    def spin(self):
        self.ball = random.choice(self.pockets)
    def betPocket(self, pocket, amt):
        if str(pocket) == str(self.ball):
            return amt*self.pocketOdds
        else:
            return - amt
    def __str__(self):
        return "Fair Roulette"

def playRoulette(game ,numSpins, pocket, bet, toPrint=True):
    totPocket = 0
    for i in range(numSpins):
        game.spin() # do the spin
        totPocket += game.betPocket(pocket, bet) # (0->lost, 35->won)
    if toPrint:
        print(numSpins, 'spins of', game)
        print('Expected return betting', pocket, '=',
            str(100*totPocket/numSpins) + '%\n')
    return (totPocket/numSpins)

# random.seed(0)
# game = FairRoulette()
# # 100->short term->high variance(what make people attract to gambling), 
# # 1000000->long term->low variance(reason why casino owner open the gambling business)
# for numSpins in (100, 1000000): 
#     for i in range(3):
#         playRoulette(game, numSpins, 2, 1, True)

# In real casino they add a green color on the Roulette 
# which make the casino's owner have more odd on the table in the long run.
# European Roulette sneak 1 green label(0) on the Roulette.
# American Roulette sneak 2 green label(0, 00) on the Roulette.
# Let's simulate this!
class EuRoulette(FairRoulette):
    def __init__(self):
        FairRoulette.__init__(self)
        self.pockets.append('0')
    def __str__(self):
        return 'European Roulette'

class AmRoulette(EuRoulette):
    def __init__(self):
        EuRoulette.__init__(self)
        self.pockets.append('00')
    def __str__(self):
        return 'American Roulette'

# Simulate the result of each type of Roulette
# random.seed(0)
# game = FairRoulette()
# eu_game = EuRoulette()
# am_game = AmRoulette()
# for numSpins in (100, 1000000): 
#     for i in range(3):
#         playRoulette(game, numSpins, 2, 1, True)
#         playRoulette(eu_game, numSpins, 2, 1, True)
#         playRoulette(am_game, numSpins, 2, 1, True)



# Applying Empirical Rule on Roulette Game (get a confidence interval)
# Empircial Rule:
# ~68% of data within 1 standard deviation of mean
# ~95% of data within 1.96 standard deviation of mean <-- we use 95% confidence
# ~99.7% of data within 3 standard deviation of mean
resultDict = {}
games = (FairRoulette, EuRoulette, AmRoulette)
numTrials = 20

def findPocketReturn(game, numTrials, trialSize, toPrint):
    pocketReturns = []
    for t in range(numTrials):
        trialVals = playRoulette(game, trialSize, 2, 1, toPrint)
        pocketReturns.append(trialVals)
    return pocketReturns
             
def getMeanAndStd(X):
    mean = sum(X)/float(len(X))
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    std = (tot/len(X))**0.5
    return mean, std


# for G in games:
#     resultDict[G().__str__()] = []
# for numSpins in (100, 1000, 10000):
#     print('\nSimulate betting a pocket for', numTrials, 'trials of',
#     numSpins, 'spins each')
#     for G in games:
#         pocketReturns = findPocketReturn(G(), 20, numSpins, False)
#         mean, std = getMeanAndStd(pocketReturns)
#         resultDict[G().__str__()].append((numSpins, 100*mean, 100*std))

#         print('Exp. return for', G(), '=', str(round(100*mean,3)) + 
#         '%', '+/- ' + str(round(100*1.96*std, 3)) + "% with 95% confidence") # use 95% confidence that's why we x1.96 to the std


# Applying CLT to Roulette
numTrials = 10000
numSpins = 20
game = FairRoulette()

means = []
for i in range(numTrials):
    means.append(findPocketReturn(game, 1, numSpins, False)[0])

plt.hist(means, bins=19, weights=[1/len(means)]*len(means))
plt.xlabel('Mean Return')
plt.ylabel('Probability')
plt.title('Expected Return Betting a Pocket 200 Times')
plt.show()