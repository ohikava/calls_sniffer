from telethon import TelegramClient, events
from loguru import logger
from telethon.events.newmessage import EventCommon
from typing import List
from dotenv import dotenv_values
import json 
from utils import extractTokenAddress, filterNonTokens
import requests

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

        extracted = extractTokenAddress(msg)
        solana_addresses = extracted['solana']
        eth_addresses = extracted['eth']

        res = []
        for address in solana_addresses:
            # if not filterNonTokens(address):
            #     continue 
            res.append({
                "channel": url,
                "msg": msg,
                "CA": address,
                "network": "SOLANA"
            })

        for address in eth_addresses:
            # if not filterNonTokens(address, net="ETH"):
            #     continue 
            res.append({
                "channel": url,
                "msg": msg,
                "CA": address,
                "network": "ETH"
            })
        if res:
            with open("save.jsonl", "a") as file:
                for i in res:
                    file.write(json.dumps(i) + "\n")

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
