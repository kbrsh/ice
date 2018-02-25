from ..random import random
from ..color import colors, colorsLength
from ..operations import operation

# Configuration
maxOperationsLength = 7

# Pixel Generator
def generatePixel(amount, color):
    pixel = []
    currentOperationsLength = (random() % maxOperationsLength) + 1

    for i in range(amount):
        pixel.append(operation(currentOperationsLength))

    if color:
        pixel.append(colors[random() % colorsLength])

    return pixel
