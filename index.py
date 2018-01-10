import os
import time
import png
import TwitterAPI
import src.loader
import src.seed
import src.pixel

# Configuration
rows = 1000
cols = 1000
twitterAPI = TwitterAPI.TwitterAPI(
    consumer_key=os.environ["CONSUMER_KEY"],
    consumer_secret=os.environ["CONSUMER_SECRET"],
    access_token_key=os.environ["ACCESS_TOKEN_KEY"],
    access_token_secret=os.environ["ACCESS_TOKEN_SECRET"]
)

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
        src.loader.load(row / (rows - 1))

    f = open("art.png", "wb")
    w = png.Writer(cols, rows)
    w.write(f, data)
    f.close()

# Generate
def generate():
    seedText = src.seed.generateSeed()
    generateImage(src.pixel.generatePixel())

    f = open("art.png", "rb")
    twitterAPI.request("statuses/update_with_media", {
        "status": seedText
    }, {
        "media[]": f.read()
    })
    f.close()

    return seedText

while True:
    print("\x1b[36mIce\x1b[0m Crafting Post 💡")
    print("\x1b[36mIce\x1b[0m Success \"" + generate() + "\" ✨\n")
    time.sleep(1020)
