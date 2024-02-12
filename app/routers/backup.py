
from app import app
from app import get_not_backuped_file, add_backup_id


from telethon.sync import TelegramClient

from bot.session import get_session

import traceback
import time

import os
chat_id = os.getenv('CHAT_ID')
chat_backup = os.getenv('CHAT_BACKUP')






@app.get("/backup")
async def backup():
    files = get_not_backuped_file()

    for file in files:
        try:
            client: TelegramClient = await get_session()
            ids = []
            for msg_id in eval(file.tg_id):
                
                ids.append((await client.forward_messages(chat_backup, msg_id, chat_id)).id)

            await client.disconnect()

            ids = str(ids)

            add_backup_id(file.id, ids)
            time.sleep(1)
    
        except Exception as e:
            print(e)
            await client.disconnect()
            traceback_str = traceback.format_exc()
            print(f"Произошла ошибка: {traceback_str}")
    
    return 200