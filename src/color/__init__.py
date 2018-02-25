import colorsys
from ..random import random

# RGB
def rgb(c1, c2, c3):
    return ((c1 * 127.5) + 127.5, (c2 * 127.5) + 127.5, (c3 * 127.5) + 127.5)

# HSL
def hsl(c1, c2, c3):
    (r, g, b) = colorsys.hls_to_rgb((c1 * 0.5) + 0.5, (c3 * 0.5) + 0.5, (c2 * 0.5) + 0.5)
    return (r * 255.0, g * 255.0, b * 255.0)

# Generate
def generateColors():
    color1 = float(random()) / float(0xFFFFFFFFFFFFFFFF)
    return color1, (color1 + (float(random()) / (7.0 * float(0xFFFFFFFFFFFFFFFF)))) % 1.0

colors = [rgb, hsl]
colorsLength = len(colors)
