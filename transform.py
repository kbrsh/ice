import png
import src.seed
import src.pixel

# Intro
print("\x1b[36mIce\x1b[0m Transforming Image 💡")

# Seed
seedText = src.seed.generateSeed()

# Read
f = open("art.png", "rb")
r = png.Reader(f)
info = r.read()
width = info[0]
height = info[1]
data = list(info[2])
alpha = info[3]["alpha"]
skip = 4 if alpha else 3
f.close()

# Transform
transformSlope = 2.0 / 255.0
transformYInt = -1.0
secondSlope = 2.0 / float(width + height - 2)
secondYInt = -1.0
pixel = src.pixel.generatePixel()
pixelOperationC1 = pixel[0]
pixelOperationC2 = pixel[1]
pixelOperationC3 = pixel[2]
pixelColor = pixel[3]

for rowIndex, row in enumerate(data):
    row = list(map(float, row))
    for colIndex in range(0, len(row), skip):
        second = ((rowIndex + (colIndex / skip)) * secondSlope) + secondYInt

        r = (row[colIndex] * transformSlope) + transformYInt
        r = pixelOperationC1.compute(r, second)

        g = (row[colIndex + 1] * transformSlope) + transformYInt
        g = pixelOperationC2.compute(g, second)

        b = (row[colIndex + 2] * transformSlope) + transformYInt
        b = pixelOperationC3.compute(b, second)

        r, g, b = pixelColor(r, g, b)
        row[colIndex] = r
        row[colIndex + 1] = g
        row[colIndex + 2] = b

    data[rowIndex] = row

# Write
f = open("transform.png", "wb")
w = png.Writer(width, height, alpha=alpha)
w.write(f, data)
f.close()

# Success
print("\x1b[36mIce\x1b[0m Success \"" + seedText + "\" ✨")
