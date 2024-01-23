from telethon.sync import TelegramClient

from bot.session import get_session

from app import progress

import os
chat_id = os.getenv('CHAT_ID')

from config import CHANK_SIZE_MB

async def send_file(file, task_id):
    def callback(current, total):
        progress.set_progress(task_id, i, round(current / total_size * 100, 2))

    try:
        client: TelegramClient = await get_session()
        
        ids=[]
        total_size = file.getbuffer().nbytes
        i = 0
        while True:
            part_file = file.read(CHANK_SIZE_MB * 1024 * 1024)
            if not part_file:
                break
            print(f'send_file: {chat_id = }, {ids = }')
            file_info = await client.send_file(
                                            chat_id,
                                            part_file,
                                            use_cache=False,
                                            part_size_kb=512,
                                            progress_callback=callback,
                                            )
            ids.append(file_info.id)
            i += 1

        await client.disconnect()

        return str(ids)
    
    except Exception as e:
        print(e)
        await client.disconnect()
        return False
    


async def download_file(message_id, task_id):
    msg_count = len(eval(message_id))

    def callback(current, total):
        progress.set_progress(task_id, msg.id, round(current / total_size * 100, 2))
    
    try:
        client: TelegramClient = await get_session()
        
        blob = bytes()
        list_msg = []
        total_size = 0

        for msg_id in eval(message_id):
            message = await client.get_messages(chat_id, ids=int(msg_id))
            list_msg.append(message)
            total_size += message.media.document.size

        for msg in list_msg:    
            print(f'download_file: {chat_id = }, {msg.id = }')

            blob += await client.download_media(msg, file=bytes, progress_callback=callback)

        await client.disconnect()
        
        return blob
    
    except Exception as e:
        print(e)
        await client.disconnect()
        return False

