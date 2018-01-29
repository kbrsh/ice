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
