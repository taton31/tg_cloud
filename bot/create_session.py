from telethon import TelegramClient
from telethon.sync import TelegramClient
from dotenv import load_dotenv
load_dotenv('../.env')
import os
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')
print(api_id)



async def get_session():
    client = TelegramClient('./sessions/tg_cloud', api_id, api_hash, system_version='4.16.30-vxCUSTOM')
    client.flood_sleep_threshold = 24*60*60
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

if __name__ == '__main__':
    import asyncio
    asyncio.run(get_session())
