import openai
from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import filters
from aiogram.utils import executor

from src.infrstructure.config import settings
from src.infrstructure.log import configure_logging
from src.web.handlers.conversation import handle_conversation
from src.web.handlers.start import send_welcome


def create_dispatcher() -> Dispatcher:
    configure_logging(log_level=settings.LOG_LEVEL, log_format=settings.LOG_FORMAT)

    openai.api_key = settings.OPENAI_API_TOKEN

    bot = Bot(token=settings.TG_TOKEN)
    # storage = RedisStorage2(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD)
    dispatcher = Dispatcher(bot=bot)

    dispatcher.middleware.setup(LoggingMiddleware())

    # start handler
    dispatcher.register_message_handler(send_welcome, filters.CommandStart())

    # handler conversation
    dispatcher.register_message_handler(handle_conversation)

    return dispatcher


dp = create_dispatcher()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
