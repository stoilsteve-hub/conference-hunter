with open("new_urls_mega.txt") as f:
    urls_code = f.read()

code = f"""import time
from core.engine import Engine

class Launcher:
    def __init__(self):
        self.engine = Engine()
        print("Bot initialized...")

    def start(self):
        print("Bot starting up...")
{urls_code}
        self.engine.run()
        print("Bot finished!")

    def stop(self):
        print("Bot stopped!")

if __name__ == "__main__":
    bot = Launcher()
    bot.start()
"""

with open("main.py", "w") as f:
    f.write(code)
