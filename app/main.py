import asyncio
import os
from pathlib import Path

from dotenv import dotenv_values
from redis.asyncio import Redis
from telethon import events, TelegramClient

from app.handlers.new_message import handler as new_message_handler


async def main() -> None:
    curr_dir = Path(os.getcwd())
    sources_file = curr_dir.joinpath("sources.txt")
    
    with open(sources_file) as reader:
        urls = reader.readlines()

    secrets = dotenv_values(".env")

    API_ID = secrets["API_ID"]
    API_HASH = secrets["API_HASH"]
    TG_TOKEN = secrets["TG_TOKEN"]

    client = TelegramClient("anon", API_ID, API_HASH)

    redis_client = Redis(host="localhost", port=6379)

    client.add_event_handler(new_message_handler(redis_client), events.NewMessage(chats=urls))

    await client.start()
    await client.run_until_disconnected()

    await redis_client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
