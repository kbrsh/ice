import os
import time
import TwitterAPI
import src.art.fluid
import src.art.gas
import src.art.map

# Configuration
twitterAPI = TwitterAPI.TwitterAPI(
    consumer_key=os.environ["CONSUMER_KEY"],
    consumer_secret=os.environ["CONSUMER_SECRET"],
    access_token_key=os.environ["ACCESS_TOKEN_KEY"],
    access_token_secret=os.environ["ACCESS_TOKEN_SECRET"]
)

# Generate
types = [src.art.fluid, src.art.gas, src.art.map]
totalTypes = len(types)
current = 0
while True:
    print("\x1b[36mIce\x1b[0m Crafting Post 💡")

    seedText = types[current].generate()
    f = open("art.png", "rb")
    twitterAPI.request("statuses/update_with_media", {
        "status": seedText
    }, {
        "media[]": f.read()
    })
    f.close()

    print("\x1b[36mIce\x1b[0m Success \"" + seedText + "\" ✨\n")
    current = (current + 1) % totalTypes
    time.sleep(1020)
