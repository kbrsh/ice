import math
import colorsys
import png
import src.loader
import src.seed
import src.random

# Configuration
width = 1000
height = 1000

# Initialize
print("\x1b[36mIce\x1b[0m Crafting Trail 💡")
seedText = src.seed.generateSeed()
data = []

for y in range(height):
    current = []

    for x in range(width):
        current.append(0.0)
        current.append(0.0)
        current.append(0.0)

    data.append(current)

# Colors
color1 = float(src.random.random()) / float(0xFFFFFFFFFFFFFFFF)
color2 = color1 + ((float(4.0 * src.random.random()) / (21.0 * float(0xFFFFFFFFFFFFFFFF))) + (1.0 / 7.0))
if color2 > 1.0:
    color2 = 1.0

lums = {}

# Put
def put(x, y):
    x = x * 3
    y = height - y - 1

    lum = lums.get((x, y))

    if lum is None:
        lum = lums[(x, y)] = 0.07
    else:
        lum = lums[(x, y)] = lum + 0.07

    if lum > 0.7:
        lum = 0.7

    colorHue = (color2 - color1) * src.random.randomNoise2(x / 500, y / 500) + color1
    (r, g, b) = colorsys.hls_to_rgb(colorHue, lum, 1.0)

    row = data[y]
    row[x] = r * 255.0
    row[x + 1] = g * 255.0
    row[x + 2] = b * 255.0

def putClear(x, y):
    x = x * 3
    y = height - y - 1

    row = data[y]
    row[x] = 0.0
    row[x + 1] = 0.0
    row[x + 2] = 0.0

# Sizes, offsets, points, vectors, and time configuration
xs = 700
ys = 700

xo = int((width - xs) / 2)
yo = int((height - ys) / 2)

p = []
v = []
o = 10
tt = 1000

# Vectors
for x in range(0, width):
    vcol = []
    v.append(vcol)

    for y in range(0, height):
        angle = 2 * math.pi * src.random.randomNoise2(x / 500, y / 500)
        vcol.append([math.cos(angle), math.sin(angle)])

# Points
for x in range(xo, xo + xs, o):
    pcol = []
    p.append(pcol)
    for y in range(yo, yo + ys, o):
        pcol.append([x, y])

# Movement
for t in range(tt):
    for pcol in p:
        for pc in pcol:
            x = pc[0] % width
            y = pc[1] % height

            vc = v[x][y]
            vx = vc[0]
            vy = vc[1]

            pc[0] = x + round(vx)
            pc[1] = y + round(vy)

            put(x, y)
    src.loader.load(t / (tt - 1))

# Clear
for x in range(0, width):
    for y in range(0, height):
        if x < xo or x >= (xo + xs) or y < yo or y >= (yo + ys):
            putClear(x, y)

# Write
f = open("art.png", "wb")
w = png.Writer(width, height)
w.write(f, data)
f.close()

print("\x1b[36mIce\x1b[0m Success \"" + seedText + "\" ✨\n")
