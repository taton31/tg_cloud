from telethon import TelegramClient
from telethon.sync import TelegramClient

import os
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')




async def get_session():
    client = TelegramClient('bot\sessions\\tg_cloud', api_id, api_hash, system_version='4.16.30-vxCUSTOM')
    await client.connect()
    if not await client.is_user_authorized():
        try:
            await client.start(phone_number)
        except Exception as e:
            print(f"Error connecting: {e}")
            return

        print("Successfully connected.")

        me = await client.get_me()
        print(f'Connected as {me.username}')

    return client

