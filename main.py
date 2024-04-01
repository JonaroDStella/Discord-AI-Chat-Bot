from utils.Bots import CentralBot
from config import *

if __name__ == '__main__':
    bot = CentralBot(command_prefix=COMMAND_PREFIX, cogs_dir='cogs\\')
    bot.run(TOKEN)