from typing import Awaitable, Callable

from redis.asyncio import Redis
from telethon import events


def handler(redis: Redis) -> Callable[[events.NewMessage], Awaitable[None]]:
    async def wrapped(event: events.NewMessage) -> None:
        ...

    return wrapped

