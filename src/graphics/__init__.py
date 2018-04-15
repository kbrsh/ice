import colorsys
import png
from ..random import randomNoise2D

# Configuration
width = 1000 # Width
height = 1000 # Height
xs = 700 # Filled width
ys = 700 # Filled height

xo = int((width - xs) / 2) # X filled offset margins
yo = int((height - ys) / 2) # Y filled offset margins

# Generate data
def generateData():
    data = []

    for y in range(height):
        current = []

        for x in range(width):
            current.append(0.0)
            current.append(0.0)
            current.append(0.0)

        data.append(current)

    return data

# Generate points
def generatePoints(o):
    p = []

    for x in range(xo, xo + xs, o):
        pcol = []
        p.append(pcol)
        for y in range(yo, yo + ys, o):
            pcol.append([x, y])

    return p

# Put pixel
def put(x, y, c, data):
    x = int(x % width) * 3
    y = height - int(y % height) - 1

    row = data[y]
    row[x] = c[0]
    row[x + 1] = c[1]
    row[x + 2] = c[2]

# Put colored pixel
def putColor(x, y, data, hue, sat, lum):
    x = int(x % width) * 3
    y = height - int(y % height) - 1

    (r, g, b) = colorsys.hls_to_rgb(hue, lum, sat)

    row = data[y]
    row[x] = r * 255.0
    row[x + 1] = g * 255.0
    row[x + 2] = b * 255.0

# Put mixed colored pixel
def putColorMix(x, y, data, color1, color2, lums):
    x = int(x % width) * 3
    y = height - int(y % height) - 1

    lum = lums.get((x, y))

    if lum is None:
        lum = lums[(x, y)] = 0.17
    else:
        lum = lums[(x, y)] = lum + 0.17

    if lum > 0.7:
        lum = 0.7

    colorHue = (color2 - color1) * randomNoise2D(x / 500, y / 500) + color1
    (r, g, b) = colorsys.hls_to_rgb(colorHue, lum, 1.0)

    row = data[y]
    row[x] = r * 255.0
    row[x + 1] = g * 255.0
    row[x + 2] = b * 255.0

# Clear
def putClear(x, y, data):
    put(x, y, (0.0, 0.0, 0.0), data)

# Clear margins
def clearMargins(data):
    for x in range(0, width):
        for y in range(0, height):
            if x < xo or x >= (xo + xs) or y < yo or y >= (yo + ys):
                putClear(x, y, data)

# Write image
def writeImage(data):
    f = open("art.png", "wb")
    w = png.Writer(width, height)
    w.write(f, data)
    f.close()
