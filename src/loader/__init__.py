# Progress Loader
def load(percent):
    step = round(percent * 25.0)
    end = " ⚡️\n" if percent == 1.0 else ""
    print("\r\x1b[36mIce\x1b[0m Processing [" + ("=" * step) + (" " * (20 - step)) + "] " + "{0:04.1f}%".format(percent * 100.0), end=end)
