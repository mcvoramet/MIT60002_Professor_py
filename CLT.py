# Central Limit Theorem (CLT)
# Checking CLT for continuous die

import random 
import matplotlib.pyplot as plt
from monte_carlo import getMeanAndStd
import numpy as np

def plotMeans(numDice, numRolls, numBins, legend, color, style):
    means = []
    for i in range(numRolls//numDice): # meaning -> as numDice increasing the samples will reduce
        vals = 0
        for j in range(numDice):
            vals += 5*random.random() # random.random() return value between 0 and 1 (dice can be value in 0 to 5 in this case)
        means.append(vals/float(numDice))
    plt.hist(means, numBins, color = color, label = legend, weights=np.array(len(means)*[1])/len(means), hatch=style)
    return getMeanAndStd(means)

mean, std = plotMeans(1 ,1000000, 19, '1 die', 'b', '*')
print('Mean of rolling 1 dice =', str(mean) + ',', 'Std =', std)
mean, std = plotMeans(50, 100000, 19, 'Mean of 50 dice', 'r', '//')
print('Mean of rolling 5 dice =', str(mean) + ',', 'Std =', std)
plt.title('Rolling Continuous Dice')
plt.xlabel('Vale')
plt.ylabel('Probability')
plt.legend()
plt.show()


