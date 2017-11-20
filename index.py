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
maxExpressionLength = 10
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

# Expressions
class VariableX(object):
    def compute(self, x, y):
        return (x, x, x)

class VariableY(object):
    def compute(self, x, y):
        return (y, y, y)

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
        self.exponent = randomConstant()

    def compute(self, x, y):
        exponent = self.exponent
        (ar, ag, ab) = self.a.compute(x, y)

        if ar == 0:
            ar = 1
        if ag == 0:
            ag = 1
        if ab == 0:
            ab = 1

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

expressionsEnd = [VariableX, VariableY, Constant]
expressions = [Linear, Exponent, Add, Subtract, Multiply, Sin, Cos]

expressionsEndLength = len(expressionsEnd)
expressionsLength = len(expressions)

def expression(current):
    if current == 0:
        return expressionsEnd[random() % expressionsEndLength]()
    else:
        nextLevel = current - 1
        currentExpression = expressions[random() % expressionsLength]

        params = []
        paramsLength = currentExpression.__init__.__code__.co_argcount

        for param in range(paramsLength - 1):
            params.append(expression(nextLevel))

        return currentExpression(*params)

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
    pixel = expression((random() % maxExpressionLength) + 1)
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
