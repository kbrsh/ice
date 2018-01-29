import numpy as np
np.seterr(over="ignore")

# Slash
prime = np.uint64(0xA01731A5AC74E8DB)
eight = np.uint64(8)
fiftysix = np.uint64(56)

def slash(key):
    result = np.uint64(key) * prime
    result = (result >> eight) | (result << fiftysix)
    return result.item()

# Random
seed = (slash(ord('I')) + slash(ord('c')) + slash(ord('e'))) / 3
frequency = 10.0
period = 100
noiseValues = []
maximumSlopePixel = 2.0 / float(0xFFFFFFFFFFFFFFFF)
maximumSlopeConstant = 14.0 / float(0xFFFFFFFFFFFFFFFF)

def seedRandom(newSeed):
    global seed
    for i in range(period):
        noiseValues.append(float(random()) / float(0xFFFFFFFFFFFFFFFF))
    seed = newSeed

def random():
    global seed
    seed = slash(seed)
    return seed

def randomConstant():
    return (maximumSlopeConstant * float(random())) - 7.0

def noise(x):
    # Frequency
    x = x * frequency

    # Floor to integer
    xi = int(x)

    # Find output values
    xp = xi % period
    ya = noiseValues[xp]
    yb = noiseValues[xp if xp == period - 1 else xp + 1]

    # Map x -> [0, 1]
    x = x - xi

    # Smoothly map x : [0, 1] -> [ya, yb]
    return (x * x * x * (x * (x * (6.0 * yb - 6.0 * ya) + (15.0 * ya - 15.0 * yb)) + (10.0 * yb - 10.0 * ya)) + ya)
