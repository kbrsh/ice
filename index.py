import os
import math
import time
import colorsys
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
maxOperationsLength = 7
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
vowels = ['a', 'e', 'i', 'o', 'u']

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

    invalid = False
    for i, char in enumerate(seed[:-2]):
        if char not in vowels and seed[i + 1] not in vowels and seed[i + 2] not in vowels:
            invalid = True

    if invalid or seed in words or seedLength <= minSeedSize:
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
maximumSlopePixel = 2.0 / float(0xFFFFFFFFFFFFFFFF)
maximumSlopeConstant = 14.0 / float(0xFFFFFFFFFFFFFFFF)

def random():
    global seed
    value = slash(seed)
    seed = [(value >> 56) & 0xFF, (value >> 48) & 0xFF, (value >> 40) & 0xFF, (value >> 32) & 0xFF, (value >> 24) & 0xFF, (value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF]
    return value

def randomConstant():
    return (maximumSlopeConstant * float(random())) - 7.0

# Colors
def rgb(c1, c2, c3):
    return ((c1 * 127.5) + 127.5, (c2 * 127.5) + 127.5, (c3 * 127.5) + 127.5)

def hsl(c1, c2, c3):
    (r, g, b) = colorsys.hls_to_rgb((c1 * 0.5) + 0.5, (c3 * 0.5) + 0.5, (c2 * 0.5) + 0.5)
    return (r * 255.0, g * 255.0, b * 255.0)

colors = [rgb, hsl]
colorsLength = len(colors)

# Operations
class VariableXOperator(object):
    def compute(self, x, y):
        return x

class VariableYOperator(object):
    def compute(self, x, y):
        return y

class ConstantOperator(object):
    def __init__(self):
        self.constant = (maximumSlopePixel * float(random())) - 1.0

    def compute(self, x, y):
        return self.constant

class LinearOperator(object):
    def __init__(self, a):
        self.a = a
        self.slope = randomConstant()
        self.yint = randomConstant()

    def compute(self, x, y):
        return ((self.a.compute(x, y) * self.slope) + self.yint) % 1.0

class ExponentOperator(object):
    def __init__(self, a):
        self.a = a
        self.exponent = abs(randomConstant())

    def compute(self, x, y):
        ac = self.a.compute(x, y)
        if ac < 0:
            return -(abs(ac) ** self.exponent)
        else:
            return ac ** self.exponent

class AdditionOperator(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def compute(self, x, y):
        return (self.a.compute(x, y) + self.b.compute(x, y)) / 2.0

class SubtractionOperator(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def compute(self, x, y):
        return (self.a.compute(x, y) - self.b.compute(x, y)) / 2.0

class MultiplicationOperator(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def compute(self, x, y):
        return self.a.compute(x, y) * self.b.compute(x, y)

class SineOperator(object):
    def __init__(self, a):
        self.a = a
        self.frequency = randomConstant() * math.pi
        self.phase = randomConstant()

    def compute(self, x, y):
        return math.sin((self.frequency * self.a.compute(x, y)) + self.phase)

class CosineOperator(object):
    def __init__(self, a):
        self.a = a

    def compute(self, x, y):
        return math.cos(self.a.compute(x, y) * math.pi)

class HyperbolicTangentOperator(object):
    def __init__(self, a):
        self.a = a

    def compute(self, x, y):
        return math.tanh(self.a.compute(x, y))

class SquashOperator(object):
    def __init__(self, a):
        self.a = a

    def compute(self, x, y):
        ac = self.a.compute(x, y)
        return ac / (abs(ac) + 1.0)

class ArrowOperator(object):
    def __init__(self, a):
        self.a = a

    def compute(self, x, y):
        return -abs(2.0 * self.a.compute(x, y)) + 1.0

operationsEnd = [VariableXOperator, VariableYOperator, ConstantOperator]
operations = [LinearOperator, ExponentOperator, AdditionOperator, SubtractionOperator, MultiplicationOperator, SineOperator, CosineOperator, HyperbolicTangentOperator, SquashOperator, ArrowOperator]

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
    rowsSlope = 2.0 / (float(rows) - 1.0)
    colsSlope = 2.0 / (float(cols) - 1.0)
    pixelOperationC1 = pixel[0]
    pixelOperationC2 = pixel[1]
    pixelOperationC3 = pixel[2]
    pixelColor = pixel[3]

    for row in range(rows):
        currentRow = []
        x = (rowsSlope * float(row)) - 1.0

        for col in range(cols):
            y = (colsSlope * float(col)) - 1.0
            c1 = pixelOperationC1.compute(x, y)
            c2 = pixelOperationC2.compute(x, y)
            c3 = pixelOperationC3.compute(x, y)

            (r, g, b) = pixelColor(c1, c2, c3)

            currentRow.append(r)
            currentRow.append(g)
            currentRow.append(b)

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

    currentOperationsLength = (random() % maxOperationsLength) + 1
    pixel = [operation(currentOperationsLength), operation(currentOperationsLength), operation(currentOperationsLength), colors[random() % colorsLength]]

    generateImage()

    f = open("art.png", "rb")
    twitterAPI.request("statuses/update_with_media", {
        "status": seedText
    }, {
        "media[]": f.read()
    })
    f.close()

    return seedText

while True:
    print("\x1b[36mIce\x1b[0m Crafting Post 💡")
    print("\x1b[36mIce\x1b[0m Success \"" + generate() + "\" ✨")
    time.sleep(1800)
