import random
import matplotlib.pyplot as plt

dist, numSamples = [], 1000000

for i in range(numSamples):
    dist.append(random.gauss(0, 100)) # (mean=0, std=100)

weights = [1/numSamples]*len(dist)
v = plt.hist(dist, bins=100, weights=weights)

plt.xlabel('x')
plt.ylabel('Relative Frequency')
plt.title(f"Fraction within ~200 of mean = {str(sum(v[0][30:70]))}")
plt.show()