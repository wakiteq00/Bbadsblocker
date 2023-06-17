import json
from concurrent.futures import ThreadPoolExecutor
import time
from telethon import TelegramClient, events
import telethon
import asyncio
import requests

async def main():
    with open('tokens.json', 'r') as f:
        tokens = json.load(f)
    for token in tokens:
        bot_token = token["token"]
        apikey = token["apikey"]
        apihash = token["apihash"]
        chat_id = int(bot_token.split(':')[0])
        asyncio.create_task(run_client(bot_token, chat_id,apikey,apihash))
    while True:
        await asyncio.sleep(5)

async def run_client(bot_token, chat_id,apikey,apihash):
    while True:
        try:
            client = TelegramClient(''+bot_token,apikey, apihash)
            await client.start(bot_token=bot_token)

            @client.on(events.NewMessage(chats=chat_id))
            async def my_event_handler(event):
                if event.message.from_id.user_id == chat_id:
                    if '#AD' in event.message.message or '#paid-AD' in event.message.message or '#PAIDAD' in event.message.message or '#ad' in event.message.message or '#paidad' in event.message.message or '#paidAD' in event.message.message or 'bots.business/ads' in event.message.message or '#PaidAd' in event.message.message or 'sponsored' in event.message.message:
                        print(event)
                        await client.delete_messages(event.message.peer_id.user_id, event.message.id)
                        print('message deleted successfully')
                    else:
                        print('failed')
                        pass
            client.add_event_handler(my_event_handler)
            await client.run_until_disconnected()
        except telethon.errors.rpcerrorlist.AccessTokenInvalidError:
            # Send a request to a URL to remove the invalid token
            requests.get(f'https://bb-ad-blocker.vercel.app/remove2={bot_token}/apikey={apikey}/apihash={apihash}')
            
            print(bot_token)
            # Wait for some time before trying again
            await asyncio.sleep(5)
        except telethon.errors.rpcerrorlist.AccessTokenExpiredError:
            # Send a request to a URL to remove the invalid token
            
            # Wait for some time before trying again
            await asyncio.sleep(50000)
        except telethon.errors.rpcerrorlist.ApiIdInvalidError:
            # Send a request to a URL to remove the invalid token
            
            # Wait for some time before trying again
            await asyncio.sleep(50000)
        except Exception as e:
            print(e)
            await asyncio.sleep(5)

if __name__ == '__main__':
    asyncio.run(main())

