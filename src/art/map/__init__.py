import math
from ...loader import load
from ...color import generateColors
from ...seed import generateSeed
from ...random import random, randomNoise2DOctaves
from ...graphics import generateData, generatePoints, putColor, clearMargins, writeImage

# Generate
def generate():
    # Initialize
    seedText = generateSeed() # Seed
    data = generateData() # Image data
    p = generatePoints(1) # Points
    color1, color2 = generateColors()
    heights = {} # Heights
    coasts = [] # Coasts
    level = 0.5 # Level

    # Height Map
    for pcol in p:
        for pc in pcol:
            x = pc[0]
            y = pc[1]

            height = heights[(x, y)] = randomNoise2DOctaves(x / 1000.0, y / 1000.0)

            if height <= level:
                putColor(x, y, data, color1, 0.5, 0.75)

            if height > level:
                putColor(x, y, data, color2, 0.5, 0.7 - 0.4 * (height - level) / (1.0 - level))

    # Coasts
    for pcol in p:
        for pc in pcol:
            x = pc[0]
            y = pc[1]

            if heights[(x, y)] <= level and (heights.get((x + 1, y), -1) > level or heights.get((x + 1, y - 1), -1) > level or heights.get((x, y - 1), -1) > level or heights.get((x - 1, y - 1), -1) > level or heights.get((x - 1, y), -1) > level or heights.get((x - 1, y + 1), -1) > level or heights.get((x, y + 1), -1) > level or heights.get((x + 1, y + 1), -1) > level):
                coasts.append((x, y))
                putColor(x, y, data, 0.0, 0.0, 0.0)

    # Rivers
    for river in range(0, 75):
        riverLength = int(100 * random() / 0xFFFFFFFFFFFFFFFF)
        x, y = coasts[int(len(coasts) * random() / 0xFFFFFFFFFFFFFFFF)]

        currentHeight = heights[(x, y)]
        putColor(x, y, data, 0.0, 0.0, 0.0)

        for part in range(0, riverLength):
            va = 2.0 * math.pi * currentHeight
            x += math.cos(va)
            y += math.sin(va)

            xi = int(x)
            yi = int(y)

            currentHeight = heights.get((xi, yi), None)
            if currentHeight is None or currentHeight <= level:
                break
            else:
                coasts.append((xi, yi))
                putColor(x, y, data, 0.0, 0.0, 0.0)

        # for part in range(0, riverHalfLength):
        #     putColor(x, y, data, 0.0, 0.0, 0.0)
        #
        #     nextHeightCoordinates = [(x + 1, y), (x + 1, y - 1), (x, y - 1), (x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
        #     nextHeights = [heights.get(nextHeightCoordinate, -1) for nextHeightCoordinate in nextHeightCoordinates]
        #
        #     x, y = nextHeightCoordinates[nextHeights.index(max(nextHeights))]
        #
        #     currentHeight = heights.get((x, y), None)
        #     if currentHeight is None or currentHeight <= level:
        #         break

    # Mountains
    for pcolIndex in range(0, len(p), 20):
        pcol = p[pcolIndex]
        for pcIndex in range(0, len(pcol), 20):
            pc = pcol[pcIndex]
            x = pc[0]
            y = pc[1]

            if heights[(x, y)] > (1.5 * level):
                putColor(x, y, data, 0.0, 0.0, 0.0)
                putColor(x + 1, y + 1, data, 0.0, 0.0, 0.0)
                putColor(x + 2, y + 2, data, 0.0, 0.0, 0.0)
                putColor(x + 3, y + 3, data, 0.0, 0.0, 0.0)
                putColor(x + 4, y + 4, data, 0.0, 0.0, 0.0)
                putColor(x + 5, y + 3, data, 0.0, 0.0, 0.0)
                putColor(x + 6, y + 2, data, 0.0, 0.0, 0.0)
                putColor(x + 7, y + 1, data, 0.0, 0.0, 0.0)
                putColor(x + 8, y, data, 0.0, 0.0, 0.0)

    # Clear margins
    clearMargins(data)

    # Write
    writeImage(data)

    return seedText
