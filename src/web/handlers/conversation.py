import asyncio

import openai
from aiogram import types
from aiogram.types import Message
from openai.openai_object import OpenAIObject


async def handle_conversation(message: Message):
    conf = {
        "model": "text-davinci-003",
        "prompt": f"{message.text}.\n",
        "temperature": 0.5,
        "max_tokens": 3500,
    }
    output: OpenAIObject = await asyncio.to_thread(openai.Completion.create, **conf)

    await types.ChatActions.typing(sleep=0.5)

    await message.answer(output.choices.pop().text)
