from ...loader import load
from ...seed import generateSeed
from ...pixel import generatePixel
from ...graphics import width, height, generateData, put, clearMargins, writeImage

# Generate
def generate():
    seedText = generateSeed() # Seed
    data = generateData() # Image data

    # Pixel
    pixel = generatePixel(3, True)
    pixelOperationC1 = pixel[0]
    pixelOperationC2 = pixel[1]
    pixelOperationC3 = pixel[2]
    pixelColor = pixel[3]

    # Compute pixels
    for x in range(width):
        xi = (2.0 * x) / (width - 1.0) - 1.0

        for y in range(height):
            yi = (2.0 * y) / (height - 1.0) - 1.0
            put(x, y, pixelColor(pixelOperationC1.compute(xi, yi), pixelOperationC2.compute(xi, yi), pixelOperationC3.compute(xi, yi)), data)

        load(x / (width - 1))

    # Clear margins
    clearMargins(data)

    # Write
    writeImage(data)

    return seedText
