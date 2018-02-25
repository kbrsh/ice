import math
from ...loader import load
from ...color import generateColors
from ...seed import generateSeed
from ...random import randomNoise2D
from ...graphics import generateData, generatePoints, putColor, clearMargins, writeImage

# Generate
def generate():
    # Initialize
    seedText = generateSeed() # Seed
    data = generateData() # Image data
    p = generatePoints() # Points
    color1, color2 = generateColors() # Colors
    lums = {} # Color lightnesses
    tt = 1000 # Total time

    # Movement
    for t in range(tt):
        for pcol in p:
            for pc in pcol:
                x = pc[0]
                y = pc[1]

                va = 2.0 * math.pi * randomNoise2D(x / 500.0, y / 500.0)
                vx = math.cos(va)
                vy = math.sin(va)

                pc[0] = x + vx
                pc[1] = y + vy

                putColor(x, y, data, color1, color2, lums)
        load(t / (tt - 1))

    # Clear margins
    clearMargins(data)

    # Write
    writeImage(data)

    return seedText
