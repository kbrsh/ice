import numpy as np
from ..random import slash, random, seedRandom

# Configuration
gramLength = 2
minSeedSize = 2
maxSeedSize = 7
maxSeedWords = 7

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

def generateSeedText():
    gram = np.random.choice(list(model.keys()), 1)[0]
    seed = gram
    seedLength = 1

    while gram in model and seedLength <= maxSeedSize:
        gram = pickChar(model[gram])

        if gram == ' ':
            break
        else:
            seed += gram
            seedLength += 1

    invalid = False
    for i, char in enumerate(seed[:-2]):
        if char not in vowels and seed[i + 1] not in vowels and seed[i + 2] not in vowels:
            invalid = True

    if invalid or seed in words or seedLength <= minSeedSize:
        return generateSeedText()
    else:
        return seed.title()

def generateSeed():
    seedWords = random() % maxSeedWords
    seedText = generateSeedText()
    seed = 0

    for word in range(seedWords):
        seedText += ' ' + generateSeedText()

    for char in seedText:
        seed += slash(ord(char))

    seed = seed / len(seedText)
    seedRandom(seed)

    return seedText
