from telethon.sync import TelegramClient

from bot.session import get_session

from app import progress

import os
chat_id = os.getenv('CHAT_ID')

from config import TMP_FILE_FOLDER, CHANK_SEND

async def send_file(task_id):
    def callback(current, total):
        progress.set_progress(task_id, i, round(current / total_size * 100, 2))

    try:
        client: TelegramClient = await get_session()
        
        ids=[]
        file_path = f'{TMP_FILE_FOLDER}/{task_id}'
        total_size = os.path.getsize(file_path)

        i = 0
        with open(file_path, 'rb') as file:
            while chunk := file.read(CHANK_SEND):
                print(f'send_file: {chat_id = }, {ids = }')
                file_info = await client.send_file(chat_id, file=chunk, force_document=True, progress_callback=callback,)
                ids.append(file_info.id)
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

        with open(f'{TMP_FILE_FOLDER}/{task_id}', 'wb') as f:
            for msg in list_msg:    
                await client.download_media(msg, file=f, progress_callback=callback)

        await client.disconnect()
        
        return total_size
    
    except Exception as e:
        print(e)
        await client.disconnect()
        return False

