from telethon.sync import TelegramClient

from bot.session import get_session

from bot.FastTelethon import download_file_custom as fast_download_file
from bot.FastTelethon import upload_file as fast_upload_file

from app import progress

from config import CHANK

import os
chat_id = os.getenv('CHAT_ID')


import traceback



async def send_file_cor(file, task_id, total_size):
    def callback(current, total):
        progress.set_progress(task_id, i, round(current / total_size * 100, 2))

    ids = []
    i = 1
    try:
        client: TelegramClient = await get_session()

        while total_size > 0:
            upload_file = await fast_upload_file(client, file, total_size, progress_callback=callback)
            ids.append((await client.send_file(chat_id, file=upload_file, force_document=True, progress_callback=callback,)).id)
            total_size -= CHANK
            i += 1

        # while chunk := await file.read(CHANK):
        #     # upload_file = await fast_upload_file(client, chunk, total_size, progress_callback=callback)
        #     ids.append((await client.send_file(chat_id, file=chunk, force_document=True, progress_callback=callback,)).id)
        #     # ids.append((await client.send_file(chat_id, file=chunk, force_document=True, progress_callback=callback,)).id)
        #     print(f'SEND file: {round(i*CHANK/total_size*100,2)}')
            # i += 1


        # print(r)
        # print(r.id)
        # while chunk := await file.read(CHANK):
        #     ids.append((await client.send_file(chat_id, file=chunk, force_document=True, progress_callback=callback,)).id)
        #     print(f'SEND file: {round(i*CHANK/total_size*100,2)}')
        #     i += 1

        await client.disconnect()

        return str(ids)
    
    except Exception as e:
        print(e)
        await client.disconnect()
        traceback_str = traceback.format_exc()
        print(f"Произошла ошибка: {traceback_str}")
        return False
    


async def download_file(message_id, task_id):

    def callback(current, total):
        progress.set_progress(task_id, msg_id, round(current / total_size * 100, 2))
    
    try:
        client: TelegramClient = await get_session()

        list_msg = []
        total_size = 0

        for msg_id in eval(message_id):
            message = await client.get_messages(chat_id, ids=int(msg_id))
            list_msg.append(message)
            total_size += message.media.document.size

        for msg_id in eval(message_id):
            message = await client.get_messages(chat_id, ids=int(msg_id))
            async for j in fast_download_file(client, message.document, progress_callback=callback):
                yield j
            # yield await client.download_media(message, file=bytes, progress_callback=callback)
            print(f'DOWNLOAD file: {msg_id}')


        await client.disconnect()
        
    
    except Exception as e:
        print(e)
        print(e.with_traceback())
        await client.disconnect()

