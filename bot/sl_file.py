from telethon.sync import TelegramClient

from bot.session import get_session

from app import progress

from config import CHANK

import os
chat_id = os.getenv('CHAT_ID')


async def send_file_cor(file, task_id, total_size):
    def callback(current, total):
        progress.set_progress(task_id, i, round(current / total_size * 100, 2))

    ids = []
    i = 1
    try:
        client: TelegramClient = await get_session()

        while chunk := await file.read(CHANK):
            ids.append((await client.send_file(chat_id, file=chunk, force_document=True, progress_callback=callback,)).id)
            print(f'SEND file: {round(i*CHANK/total_size*100,2)}')
            i += 1

        await client.disconnect()

        return str(ids)
    
    except Exception as e:
        print(e)
        await client.disconnect()
        return False
    


async def download_file(message_id, task_id):

    def callback(current, total):
        progress.set_progress(task_id, msg.id, round(current / total_size * 100, 2))
    
    try:
        client: TelegramClient = await get_session()
        
        list_msg = []
        total_size = 0

        for msg_id in eval(message_id):
            message = await client.get_messages(chat_id, ids=int(msg_id))
            list_msg.append(message)
            total_size += message.media.document.size

        for msg in list_msg:    
            yield await client.download_media(msg, file=bytes, progress_callback=callback)
            print(f'DOWNLOAD file: {msg.id}')


        await client.disconnect()
        
    
    except Exception as e:
        print(e)
        await client.disconnect()

