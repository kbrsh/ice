from ..random import random
from ..color import colors, colorsLength
from ..operations import operation

# Configuration
maxOperationsLength = 7

# Pixel
def generatePixel():
    currentOperationsLength = (random() % maxOperationsLength) + 1
    return [operation(currentOperationsLength), operation(currentOperationsLength), operation(currentOperationsLength), colors[random() % colorsLength]]
