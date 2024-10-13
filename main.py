from utils.Bots import CentralBot
from config import *
from os import sep

if __name__ == '__main__':
    bot = CentralBot(command_prefix=COMMAND_PREFIX, cogs_dir='cogs'+sep)
    bot.run(TOKEN)