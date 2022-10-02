import random
import numpy as np

# Simulating the Buffon-Laplace's Method on Pi estimation (randomly drop the needles and count which landed on circle or and square)
def throwNeedles(numNeedles):
    inCircle = 0
    for Neeedles in range(1, numNeedles + 1, 1):
        x = random.random() # random.random() will return value between 0 and 1
        y = random.random()
        if (x*x + y*y)**0.5 <= 1.0:
            inCircle += 1
    return 4*(inCircle/float(numNeedles)) # Buffon-Laplace's equation

def getEst(numNeedles, numTrials):
    estimates = []
    for t in range(numTrials):
        piGuess = throwNeedles(numNeedles) # guess pi value
        estimates.append(piGuess)
    sDev = np.std(estimates)
    curEst = sum(estimates)/len(estimates) # get current estimate(mean of the estimate)
    print(f"Est. = {str(curEst)}, Std. dev. = {str(round(sDev, 6))}, Needles = {str(numNeedles)}")
    return (curEst, sDev)

def estPi(precision, numTrials):
    numNeedles = 1000
    sDev = precision
    while sDev >= precision/2:
        curEst, sDev = getEst(numNeedles, numTrials)
        numNeedles *= 2 # keep increasing the number of needles until it confidence about the esimation

    return curEst

estPi(0.005, 100) # result within range of 0.005 of True value