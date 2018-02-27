import numpy as np
np.seterr(over="ignore")

# Slash
prime = np.uint64(0xA01731A5AC74E8DB)
eight = np.uint64(8)
fiftySix = np.uint64(56)

def slash(key):
    result = np.uint64(key) * prime
    result = (result >> eight) | (result << fiftySix)
    return result.item()

# Random
seed = (slash(ord('I')) + slash(ord('c')) + slash(ord('e'))) / 3
frequency = 10.0
period = 1000
noiseValues = []
maximumSlopePixel = 2.0 / float(0xFFFFFFFFFFFFFFFF)
maximumSlopeConstant = 14.0 / float(0xFFFFFFFFFFFFFFFF)

def seedRandom(newSeed):
    global seed
    seed = newSeed
    for i in range(period * period):
        noiseValues.append(float(random()) / float(0xFFFFFFFFFFFFFFFF))

def random():
    global seed
    seed = slash(seed)
    return seed

def randomConstant():
    return (maximumSlopeConstant * float(random())) - 7.0

def randomNoise(x):
    # Frequency
    x = x * frequency

    # Floor to integer
    xi = int(x)

    # Find output values
    xp = xi % period
    oa = noiseValues[xp]
    ob = noiseValues[xp if xp == period - 1 else xp + 1]

    # Map x -> [0, 1]
    x = x - xi

    # Smoothly map x : [0, 1] -> [oa, ob]
    return (x * x * x * (x * (x * (6.0 * ob - 6.0 * oa) + (15.0 * oa - 15.0 * ob)) + (10.0 * ob - 10.0 * oa)) + oa)

def randomNoise2D(x, y):
    # Frequency
    x = x * frequency
    y = y * frequency

    # Floor to integer
    xi = int(x)
    yi = int(y)

    # Find period values
    xp = xi % period
    yp = yi % period

    # Find output values
    oa = noiseValues[xp * period + yp]
    ob = noiseValues[xp * period + (yp if yp == period - 1 else yp + 1)]
    oc = noiseValues[(xp if xp == period - 1 else xp + 1) * period + (yp if yp == period - 1 else yp + 1)]
    od = noiseValues[(xp if xp == period - 1 else xp + 1) * period + yp]

    # Map x, y -> [0, 1]
    x = x - xi
    y = y - yi

    # Smoothly map x : [0, 1] -> [oa, od]
    oad = x * x * x * (x * (x * (6 * od - 6 * oa) + (15 * oa - 15 * od)) + (10 * od - 10 * oa)) + oa

    # Smoothly map x : [0, 1] -> [ob, oc]
    obc = x * x * x * (x * (x * (6 * oc - 6 * ob) + (15 * ob - 15 * oc)) + (10 * oc - 10 * ob)) + ob

    # Smoothly map y : [0, 1] -> [oad, obc]
    return y * y * y * (y * (y * (6 * obc - 6 * oad) + (15 * oad - 15 * obc)) + (10 * obc - 10 * oad)) + oad
