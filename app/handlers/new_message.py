import pickle
from typing import Any, Awaitable, Callable

from redis.asyncio import Redis
from telethon.events.common import EventCommon

from app.utils import extract_token_address


def handler(redis: Redis) -> Callable[[EventCommon], Awaitable[None]]:
    async def wrapped(event: EventCommon) -> None:
        msg = event.raw_text

        extracted = extract_token_address(msg)
        solana_addresses = extracted["solana"]
        eth_addresses = extracted["eth"]

        res = {}
        for address in solana_addresses:
            if res.get(address) is None:
                res[address] = {
                    "channel": event.chat_id,
                    "msg": msg,
                    "network": "SOLANA",
                }
            
            res[address].append(
                {
                    "channel": event.chat_id,
                    "msg": msg,
                    "network": "SOLANA"
                }
            )

        for address in eth_addresses:
            if res.get(address) is None:
                res[address] = {
                    "channel": event.chat_id,
                    "msg": msg,
                    "network": "ETH",
                }
            
            res[address].append(
                {
                    "channel": event.chat_id,
                    "msg": msg,
                    "network": "ETH"
                }
            )

        for address, mentions in res.items():
            await redis.lpush(address, dump_mentions(mentions))

    return wrapped


def dump_mentions(mentions: list[dict[str, Any]]) -> list[bytes]:
    res = []

    for mention in mentions:
        res.append(pickle.dumps(mention))

    return res
