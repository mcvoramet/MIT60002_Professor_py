import random
import math

# Assume that each birthdate is equally likely
# 1 - (366! / ((366^N)*(366 - N)!) ;where N = number of people
# Related: Pigeon Hole Principle (If you have pigeons more than holed, 2 pigeons have to share a hole)

# Approximating using a simulation
def sameDate(numPeople, numSame):
    #possibleDates = range(366)
    #below is possibleDates when some year Feb have 29 days
    possibleDates = 4*list(range(0,57)) + [58] + 4*list(range(59, 366)) + 4*list(range(180, 270))
    birthdays = [0]*366
    for p in range(numPeople):
        birthDate = random.choice(possibleDates)
        birthdays[birthDate] += 1

    return max(birthdays) >= numSame

def birthdayProb(numPeople, numSame, numTrials): #(__, number of people share the same birthday, __)
    numHits = 0
    for t in range(numTrials):
        if sameDate(numPeople, numSame): # if samedate is True
            numHits += 1
    return numHits/numTrials

for numPeople in [10, 20, 40, 100]:
    print('For', numPeople, 'est. prob. of a shared birthday is', 
        birthdayProb(numPeople, 2, 10000)) # try change numSame to different number and inspect the result
    numerator = math.factorial(366)
    denom = (366**numPeople)*math.factorial(366-numPeople)
    print('Actual prob. for N = 100 =', 1-numerator/denom) # this is the calculation for finding 2 share birthday (can't use with 3 or ... share birthday)