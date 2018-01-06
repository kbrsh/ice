import numpy as np
np.seterr(over="ignore")

# Slash
prime = np.uint64(0xA171020315130201)
seven = np.uint64(7)
fiftyseven = np.uint64(57)

def slash(key):
    result = np.uint64(key) * prime
    result = (result >> seven) | (result << fiftyseven)
    return result.item()

# Random
seed = (slash(ord('I')) + slash(ord('c')) + slash(ord('e'))) / 3
maximumSlopePixel = 2.0 / float(0xFFFFFFFFFFFFFFFF)
maximumSlopeConstant = 14.0 / float(0xFFFFFFFFFFFFFFFF)

def seedRandom(newSeed):
    global seed
    seed = newSeed

def random():
    global seed
    seed = slash(seed)
    return seed

def randomConstant():
    return (maximumSlopeConstant * float(random())) - 7.0
