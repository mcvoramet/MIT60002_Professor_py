# Simulation of Drunk people walk

import random
import matplotlib.pyplot as plt
import numpy as np

# Immutable Type (not change!, benefit: can be use further as a key in dictionary)
class Location(object):
    def __init__(self, x, y):
        """x and y are floats"""
        self.x = x
        self.y = y
    
    def move(self, deltaX, deltaY): # return a new location
        """deltaX and deltaY are floats"""
        return Location(self.x + deltaX, self.y + deltaY)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def distFrom(self, other):
        xDist = self.x - other.getX()
        yDist = self.y - other.getY()
        return (xDist**2 + yDist**2)**0.5 

    def __str__(self):
        return '<' + str(self.x) + ', ' + str(self.y) + '>'

class Drunk(object):
    def __init__(self, name = None):
        """Assume name is a str"""
        self.name = name
    
    def __str__(self):
        if self != None:
            return self.name
        return 'Anonymous'

# there are 2 kinds of drunks people (usual(move randomly), masochist(bend toward only north))
class UsualDrunk(Drunk):
    def takeStep(self):
        stepChoices = [(0,1), (0,-1), (1,0), (-1,0)]
        return random.choice(stepChoices)

class MasochistDrunk(Drunk):
    def takeStep(self):
        stepChoices = [(0.0,1.1), (0.0, -0.9), (1.0,0.0), (-1.0,0.0)] # bias random walk (go 1.1 step north(1.1), while only go south 0.9 1/4 of the time(-0.9))
        return random.choice(stepChoices)

#---End of Immutable Type-----------------------------------------------------------------------------------------------------------------------------------------------

# Mutable Type (can chage, benefit: changing the value of the dictionary)
class Field(object):
    def __init__(self):
        self.drunks = {}

    def addDrunk(self, drunk, loc):
        if drunk in self.drunks:
            raise ValueError('Duplicate drunk')
        else:
            self.drunks[drunk] = loc # changing the value of the dictionary (mutated)
        
    def getLoc(self, drunk):
        if drunk not in self.drunks:
            raise ValueError('Drunk not in field')
        return self.drunks[drunk] # return location associated with that drunk

    def moveDrunk(self, drunk):
        if drunk not in self.drunks: # check whether the drunk is there
            raise ValueError('Drunk not in field')
        xDist, yDist = drunk.takeStep() # get the distance of the drunk
        # use move method of Location to get new location
        self.drunks[drunk] = self.drunks[drunk].move(xDist, yDist) # move drunk in the field

# Simulating a single walk
def walk(f, d, numSteps):
    """Assumes: f a Field, d a Drunk in f, and numSteps an int >= 0.
    Moves d numSteps times; returns the distance between the final location
    and the location at the start of the walk."""
    start = f.getLoc(d)
    for s in range(numSteps):
        f.moveDrunk(d)
    return start.distFrom(f.getLoc(d))

def simWalks(numSteps, numTrials, dClass): # dClass is either UsualDrunk or MasochistDrunk
    """Assumes numSteps an int >= 0, numTrials an int > 0,
    dClass a subclass of Drunk.
    Simulates numTrials walks of numSteps steps each.
    Returns a list of the final distances for each trial"""
    Homer = dClass() # drunk class name Homer
    origin = Location(0,0)
    distances = []
    for t in range(numTrials):
        f = Field()
        f.addDrunk(Homer, origin)
        distances.append(round(walk(f, Homer, numSteps), 1))

    return distances

#Put it all together to show the simulation
def drunkTest(walkLengths, numTrials, dClass): # walkLengths is a list of walk lengths
    """Assumes walkLengths a sequence of ints >= 0,
    numTrials an int > 0, dClass a subclass of Drunk
    For each number of steps in walkLengths,
    runs simWalks with numTrials walks and print results"""
    for numSteps in walkLengths:
        distances = simWalks(numSteps, numTrials, dClass)
        print(dClass.__name__, 'random walk of', numSteps, 'steps')  # Use __name__ to get name of the class
        print(' Mean =', round(sum(distances)/len(distances), 4))
        print(' Max =', max(distances), 'Min =', min(distances))
    return round(sum(distances)/len(distances), 4)


# Plot the location at end of walks between 2 class
def getFinalLocs(numSteps, numTrials, dClass):
    locs = []
    d = dClass()
    for t in range(numTrials):
        f = Field()
        f.addDrunk(d, Location(0, 0))
        for s in range(numSteps):
            f.moveDrunk(d)
        locs.append(f.getLoc(d))
    return locs

def plotLocs(drunkKinds, numSteps, numTrials):
    for dClass in drunkKinds:
        locs = getFinalLocs(numSteps, numTrials, dClass)
        xVals, yVals = [], []
        for loc in locs:
            xVals.append(loc.getX())
            yVals.append(loc.getY())
        xVals = np.array(xVals)
        yVals = np.array(yVals)
        meanX = sum(abs(xVals))/len(xVals)
        meanY = sum(abs(yVals))/len(yVals)
       
        plt.scatter(xVals, yVals,
                      label = dClass.__name__ +\
                      ' mean abs dist = <'
                      + str(meanX) + ', ' + str(meanY) + '>')
    plt.title('Location at End of Walks ('
                + str(numSteps) + ' steps)')
    plt.ylim(-1000, 1000)
    plt.xlim(-1000, 1000)
    plt.xlabel('Steps East/West of Origin')
    plt.ylabel('Steps North/South of Origin')
    plt.legend(loc = 'lower center')
    plt.show()

random.seed(0)
plotLocs((UsualDrunk, MasochistDrunk), 10000, 1000)

#---------------------------------------------------------------------------------------------------------------

# Wormhole Problem
class OddField(Field):
    def __init__(self, numHoles =1000,  xRange = 100, yRange = 100):
        Field.__init__(self)
        self.wormholes = {}
        for w in range(numHoles):
            # where wormhole located
            x = random.randint(-xRange, xRange) 
            y = random.randint(-yRange, yRange) 
            # where you teleproted to when enter the wormhole
            newX = random.randint(-xRange, yRange)
            newY = random.randint(-yRange, yRange)
            newLoc = Location(newX, newY)
            self.wormholes[(x, y)] = newLoc # update dictonary of wormhole to new location
    
    def moveDrunk(self, drunk):
        Field.moveDrunk(self, drunk)
        x = self.drunks[drunk].getX()
        y = self.drunks[drunk].getY()
        if (x, y) in self.wormholes: # if enter the wormhole
            self.drunks[drunk] = self.wormholes[(x, y)] # enter the location associated with that wormhole

# TraceWalk using oddField (Simulate Wormhole problem vs. Normal Field)          
# def traceWalk(fieldKinds, numSteps):
#     for fClass in fieldKinds:
#         d = UsualDrunk()
#         f = fClass()
#         f.addDrunk(d, Location(0, 0))
#         locs = []
#         for s in range(numSteps):
#             f.moveDrunk(d)
#             locs.append(f.getLoc(d))
#         xVals, yVals = [], []
#         for loc in locs:
#             xVals.append(loc.getX())
#             yVals.append(loc.getY())
#         plt.scatter(xVals, yVals, label=fClass.__name__)
#     plt.title(f"Spots Vistied on Walk ({str(numSteps)} steps)")
#     plt.xlabel('Steps East/West of Origin')
#     plt.ylabel('Steps North/South of Origin')
#     plt.legend()
#     plt.show()

# random.seed(0)
# traceWalk((Field, OddField), 500)
