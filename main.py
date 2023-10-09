import threading

from utils import Bots
from config import HISTORY_LIMIT, PROMPT, TOKEN, ADMIN_ID


if __name__ == '__main__':
    bot = Bots.Chat_Bot(
        prefix='$ ',
        token=TOKEN,
        prompt=PROMPT,
        voice_id=47,
        limit=HISTORY_LIMIT,
        admin_id=ADMIN_ID)
    main = threading.Thread(target=bot.main, args=[])
    main.start()
    main.join()