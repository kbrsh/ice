import png
from ...loader import load
from ...seed import generateSeed
from ...pixel import generatePixel

# Configuration
rows = 1000
cols = 1000

# Generate Image
def generateImage(pixel):
    data = []
    rowsSlope = 2.0 / (float(rows) - 1.0)
    colsSlope = 2.0 / (float(cols) - 1.0)
    pixelOperationC1 = pixel[0]
    pixelOperationC2 = pixel[1]
    pixelOperationC3 = pixel[2]
    pixelColor = pixel[3]

    for row in range(rows):
        currentRow = []
        x = (rowsSlope * float(row)) - 1.0

        for col in range(cols):
            y = (colsSlope * float(col)) - 1.0
            (c1, c2, c3) = pixelColor(pixelOperationC1.compute(x, y), pixelOperationC2.compute(x, y), pixelOperationC3.compute(x, y))

            currentRow.append(c1)
            currentRow.append(c2)
            currentRow.append(c3)

        data.append(currentRow)
        load(row / (rows - 1))

    f = open("art.png", "wb")
    w = png.Writer(cols, rows)
    w.write(f, data)
    f.close()

# Generate
def generate():
    seedText = generateSeed()
    generateImage(generatePixel())

    return seedText
