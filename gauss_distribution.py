import numpy as np
import random
import matplotlib.pyplot as plt
import scipy.integrate


def gaussian(x, mu, sigma):
    factor1 = (1.0/(sigma*((2*np.pi)**0.5)))
    factor2 = np.exp((-((x-mu)**2))/(2*sigma**2))
    return factor1 * factor2

xVals, yVals = [], []
mu, sigma = 0, 1
x = -4
while x <= 4:
    xVals.append(x)
    yVals.append(gaussian(x, mu, sigma))
    x += 0.05

# Use integral to check the empirical rule (1 std = 0.6827, 1.96 std = 0.95, 3 std = 0.9973)
def checkEmpirical(numTrials):
    for t in range(numTrials):
        mu = random.randint(-10, 10)
        sigma = random.randint(1, 10)
        print('For mu =', mu, 'and sigma =', sigma)
        for numStd in (1, 1.96, 3):
            area = scipy.integrate.quad(gaussian, mu-numStd*sigma, mu+numStd*sigma,(mu, sigma))[0]

            print('Fraction within', numStd, 'std =', round(area, 4))

checkEmpirical(3)
# plot gaussian distribution
plt.plot(xVals, yVals)
plt.title('Normal Distribution, mu = ' + str(mu) + ', sigma = ' + str(sigma))
plt.show()