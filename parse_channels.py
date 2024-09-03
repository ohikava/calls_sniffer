from time import sleep
from telethon import TelegramClient, events
from loguru import logger
from telethon.events.newmessage import EventCommon
from typing import List
from dotenv import dotenv_values
import tomllib

from utils.funcs import load_urls 
from utils.types import Config, NetworkName, State
from utils.sniper import Sniper
from utils.parser import extractTokenAddress, extractTokenInfo

with open("sources.txt") as file:
    srcs = file.readlines()

secrets = dotenv_values(".env")
API_ID = secrets["API_ID"]
API_HASH = secrets["API_HASH"]
TG_TOKEN = secrets["TG_TOKEN"]



client = TelegramClient('anon', API_ID, API_HASH)

seen = set()

def handle_messages(url: str): 
    async def _(event: EventCommon):
        msg = event.raw_text

        # DO SMTH
    return _ 

for url in srcs:
    msg_handles = handle_messages(url)
    msg_handles = client.on(events.NewMessage(chats=[url]))(msg_handles)

# @client.on(events.NewMessage(chats=[config['sniperBotNickname']]))
# async def monitorSniperBot(event):
#     if global_variables['state'] == State.WAITING_FOR_TOKEN_BUY:
#         global_variables['state'] = State.NOTHING


def start_bot():
    client.start()
    client.run_until_disconnected()

start_bot()
