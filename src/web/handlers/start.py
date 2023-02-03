import asyncio

import structlog
from aiogram import types

from src.web.messages import msg

logger = structlog.get_logger(__name__)
mutex = asyncio.Lock()


async def send_welcome(message: types.Message) -> None:
    await types.ChatActions.typing(sleep=0.5)

    await message.answer(
        text=msg.greeting.format(name=message.from_user.full_name),
    )
