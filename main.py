import time
from core.engine import Engine

class Launcher:
    def __init__(self):
        self.engine = Engine()
        print("Bot initialized...")

    def start(self):
        print("Bot starting up...")
        # give it some dummy urls to test
        self.engine.load_urls(["http://example-pharma.com", "http://another-test.com"])
        self.engine.run()
        print("Bot finished!")

    def stop(self):
        print("Bot stopped!")

if __name__ == "__main__":
    bot = Launcher()
    # Press play here in PyCharm!
    bot.start()
