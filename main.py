import time
from core.engine import Engine

class Launcher:
    def __init__(self):
        self.engine = Engine()
        print("Bot initialized...")

    def start(self):
        print("Bot starting up...")
        # give it some dummy urls to test
        self.engine.load_urls([
            "https://www.immuno-oncologyeurope.com/",
            "https://peptide-based-therapeutics-summit.com/",
            "https://cdx-europe.com/",
            "https://lnp-formulation-process-development-pharma.com/",
            "https://genetherapy-conference.com/"
        ])
        self.engine.run()
        print("Bot finished!")

    def stop(self):
        print("Bot stopped!")

if __name__ == "__main__":
    bot = Launcher()
    # Press play here in PyCharm!
    bot.start()
