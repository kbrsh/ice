import png
import math
import numpy as np
np.seterr(over="ignore")

data = open("data/data.txt").read()
words = data.split('\n')
increment = 1 / (len(data) - len(words))
model = {}

for word in words:
    if word != '\n':
        word = word + ' ';
        for i, char in enumerate(word[:-1]):
            probs = None

            if char in model:
                probs = model[char]
            else:
                probs = model[char] = {}

            nextChar = word[i + 1]
            if nextChar in probs:
                probs[nextChar] += increment
            else:
                probs[nextChar] = increment

def pickChar(info):
    chars = []
    probs = []

    for char, prob in info.items():
        chars.append(char)
        probs.append(prob)

    return np.random.choice(chars, 1, p=probs)[0]

def generateSeed():
    word = ''
    currentInfo = model.popitem()
    char = pickChar(currentInfo)
    currentInfo = currentInfo[char]

    while char != " ":
        picked = pickChar(info)
        word += picked
        currentInfo = currentInfo[picked]

    return word

print(generateSeed())
