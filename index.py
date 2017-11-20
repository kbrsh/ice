import os
import math
import time
import png
import TwitterAPI
import numpy as np
np.seterr(over="ignore")

# Configuration
gramLength = 2
minSeedSize = 2
maxSeedSize = 7
rows = 1000
cols = 1000
maxOperationLength = 10
twitterAPI = TwitterAPI.TwitterAPI(
    consumer_key=os.environ["CONSUMER_KEY"],
    consumer_secret=os.environ["CONSUMER_SECRET"],
    access_token_key=os.environ["ACCESS_TOKEN_KEY"],
    access_token_secret=os.environ["ACCESS_TOKEN_SECRET"]
)

# Model
words = open("data/data.txt").read().split('\n')
model = {}

for word in words:
    if word != '\n':
        for g in range(gramLength):
            grams = [word[i:i + gramLength] for i in range(g, len(word), gramLength)]
            grams.append(' ')
            for i, gram in enumerate(grams[:-1]):
                probs = None

                if gram in model:
                    probs = model[gram]
                    probs["total"] += 1
                else:
                    probs = model[gram] = {
                        "total": 1
                    }

                nextGram = grams[i + 1]
                if nextGram in probs:
                    probs[nextGram] += 1
                else:
                    probs[nextGram] = 1

for gram, amount in model.items():
    probs = model[gram]
    total = probs["total"]

    for nextGram, prob in probs.items():
        probs[nextGram] = prob / total

    del probs["total"]

# Seed Generator
def pickChar(info):
    grams = []
    probs = []

    for gram, prob in info.items():
        grams.append(gram)
        probs.append(prob)

    return np.random.choice(grams, 1, p=probs)[0]

def generateSeed():
    gram = np.random.choice(list(model.keys()), 1)[0]
    seed = gram
    seedLength = 1

    while gram in model and seedLength <= maxSeedSize:
        gram = pickChar(model[gram])

        if gram == " ":
            break
        else:
            seed += gram
            seedLength += 1

    if seed in words or seedLength <= minSeedSize:
        return generateSeed()
    else:
        return seed.title()

# Slash
prime = np.uint64(0xA171020315130201)
seven = np.uint64(7)
fiftyseven = np.uint64(57)

def slash(key):
    result = np.uint64(0)

    for i in range(len(key)):
        result = (result ^ np.uint64(key[i])) * (prime)
        result = (result >> seven) | (result << fiftyseven)

    return result.item()

# Random
seed = None
maximumSlope = 1.0 / (float(0xFFFFFFFFFFFFFFFF) / 2.0)
maximumSlope7 = 1.0 / (float(0xFFFFFFFFFFFFFFFF) / 14.0)

def random():
    global seed
    value = slash(seed)
    seed = [(value >> 56) & 0xFF, (value >> 48) & 0xFF, (value >> 40) & 0xFF, (value >> 32) & 0xFF, (value >> 24) & 0xFF, (value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF]
    return value

def randomPixel():
    return (maximumSlope * float(random())) - 1.0

def randomConstant():
    return (maximumSlope7 * float(random())) - 1.0

# Operations
class VariableX(object):
    def compute(self, x, y):
        return (x, x, x)

class VariableY(object):
    def compute(self, x, y):
        return (y, y, y)

class LinearX(object):
    def __init__(self):
        self.slopes = [randomConstant(), randomConstant(), randomConstant()]
        self.yints = [randomConstant(), randomConstant(), randomConstant()]
    def compute(self, x, y):
        slopes = self.slopes
        yints = self.yints
        return (((slopes[0] * x) + yints[0]) % 1.0, ((slopes[1] * x) + yints[1]) % 1.0, ((slopes[2] * x) + yints[2]) % 1.0)

class LinearY(object):
    def __init__(self):
        self.slopes = [randomConstant(), randomConstant(), randomConstant()]
        self.yints = [randomConstant(), randomConstant(), randomConstant()]
    def compute(self, x, y):
        slopes = self.slopes
        yints = self.yints
        return (((slopes[0] * y) + yints[0]) % 1.0, ((slopes[1] * y) + yints[1]) % 1.0, ((slopes[2] * y) + yints[2]) % 1.0)

class ExponentX(object):
    def __init__(self):
        self.exponents = [abs(randomConstant()), abs(randomConstant()), abs(randomConstant())]

    def compute(self, x, y):
        exponents = self.exponents
        absX = abs(x)
        return (absX ** exponents[0], absX ** exponents[1], absX ** exponents[2])

class ExponentY(object):
    def __init__(self):
        self.exponents = [abs(randomConstant()), abs(randomConstant()), abs(randomConstant())]

    def compute(self, x, y):
        exponents = self.exponents
        absY = abs(y)
        return (absY ** exponents[0], absY ** exponents[1], absY ** exponents[2])

class SinX(object):
    def __init__(self):
        self.frequencies = [randomConstant() * math.pi, randomConstant() * math.pi, randomConstant() * math.pi]
        self.phases = [randomConstant(), randomConstant(), randomConstant()]

    def compute(self, x, y):
        frequencies = self.frequencies
        phases = self.phases
        return (math.sin((frequencies[0] * x) + phases[0]), math.sin((frequencies[1] * x) + phases[1]), math.sin((frequencies[2] * x) + phases[2]))

class SinY(object):
    def __init__(self):
        self.frequencies = [randomConstant() * math.pi, randomConstant() * math.pi, randomConstant() * math.pi]
        self.phases = [randomConstant(), randomConstant(), randomConstant()]

    def compute(self, x, y):
        frequencies = self.frequencies
        phases = self.phases
        return (math.sin((frequencies[0] * y) + phases[0]), math.sin((frequencies[1] * y) + phases[1]), math.sin((frequencies[2] * y) + phases[2]))

class CosX(object):
    def compute(self, x, y):
        return (math.cos(x), math.cos(x), math.cos(x))

class CosY(object):
    def compute(self, x, y):
        return (math.cos(y), math.cos(y), math.cos(y))

class Constant(object):
    def __init__(self):
        self.constant = (randomPixel(), randomPixel(), randomPixel())
    def compute(self, x, y):
        return self.constant

class Linear(object):
    def __init__(self, a):
        self.a = a
        self.slope = randomConstant()
        self.yint = randomConstant()

    def compute(self, x, y):
        slope = self.slope
        yint = self.yint
        (ar, ag, ab) = self.a.compute(x, y)
        return (((slope * ar) + yint) % 1.0, ((slope * ag) + yint) % 1.0, ((slope * ab) + yint) % 1.0)

class Exponent(object):
    def __init__(self, a):
        self.a = a
        self.exponent = abs(randomConstant())

    def compute(self, x, y):
        exponent = self.exponent
        (ar, ag, ab) = self.a.compute(x, y)
        return (abs(ar) ** exponent, abs(ag) ** exponent, abs(ab) ** exponent)

class Add(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def compute(self, x, y):
        (ar, ag, ab) = self.a.compute(x, y)
        (br, bg, bb) = self.b.compute(x, y)
        return ((ar + br) / 2.0, (ag + bg) / 2.0, (ab + bb) / 2.0)

class Subtract(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def compute(self, x, y):
        (ar, ag, ab) = self.a.compute(x, y)
        (br, bg, bb) = self.b.compute(x, y)
        return ((ar - br) / 2.0, (ag - bg) / 2.0, (ab - bb) / 2.0)

class Multiply(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def compute(self, x, y):
        (ar, ag, ab) = self.a.compute(x, y)
        (br, bg, bb) = self.b.compute(x, y)
        return (ar * br, ag * bg, ab * bb)

class Sin(object):
    def __init__(self, a):
        self.a = a
        self.frequency = randomConstant() * math.pi
        self.phase = randomConstant()

    def compute(self, x, y):
        frequency = self.frequency
        phase = self.phase
        (ar, ag, ab) = self.a.compute(x, y)
        return (math.sin((frequency * ar) + phase), math.sin((frequency * ag) + phase), math.sin((frequency * ab) + phase))

class Cos(object):
    def __init__(self, a):
        self.a = a

    def compute(self, x, y):
        (ar, ag, ab) = self.a.compute(x, y)
        return (math.cos(ar), math.cos(ag), math.cos(ab))

operationsEnd = [VariableX, VariableY, LinearX, LinearY, ExponentX, ExponentY, SinX, SinY, CosX, CosY, Constant]
operations = [Linear, Exponent, Add, Subtract, Multiply, Sin, Cos]

operationsEndLength = len(operationsEnd)
operationsLength = len(operations)

def operation(current):
    if current == 0:
        return operationsEnd[random() % operationsEndLength]()
    else:
        nextLevel = current - 1
        currentOperation = operations[random() % operationsLength]

        params = []
        paramsLength = currentOperation.__init__.__code__.co_argcount

        for param in range(paramsLength - 1):
            params.append(operation(nextLevel))

        return currentOperation(*params)

# Pixel
pixel = None

# Generate Image
def generateImage():
    data = []
    rowsSlope = 1.0 / (float(rows) / 2.0)
    colsSlope = 1.0 / (float(cols) / 2.0)

    for row in range(rows):
        currentRow = []
        x = (rowsSlope * float(row)) - 1.0

        for col in range(cols):
            (r, g, b) = pixel.compute(x, (colsSlope * float(col)) - 1.0)
            currentRow.append((r * 127.5) + 127.5)
            currentRow.append((g * 127.5) + 127.5)
            currentRow.append((b * 127.5) + 127.5)

        data.append(currentRow)

    f = open("art.png", "wb")
    w = png.Writer(cols, rows)
    w.write(f, data)
    f.close()

# Generate
def generate():
    global seed
    global pixel

    seedText = generateSeed()
    seed = [ord(char) for char in seedText]
    pixel = operation((random() % maxOperationLength) + 1)
    generateImage()

    f = open("art.png", "rb")
    twitterAPI.request("statuses/update_with_media", {
        "status": seedText
    }, {
        "media[]": f.read()
    })
    f.close()

while True:
    generate()
    time.sleep(3600)
