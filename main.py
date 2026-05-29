import time

class Launcher:
    def __init__(self):
        print("Bot initialized...")

    def start(self):
        print("Bot starting up...")
        print("Running scraper... (not really yet lol)")
        time.sleep(2)
        print("Bot finished!")

    def stop(self):
        print("Bot stopped!")

if __name__ == "__main__":
    bot = Launcher()
    # Press play here in PyCharm!
    bot.start()
