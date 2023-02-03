import structlog
from aiogram import Dispatcher

from src.infrstructure.db_session import redis

logger = structlog.get_logger(__name__)


async def on_shutdown(dp: Dispatcher):
    logger.info("Shutting down..")

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    await redis.get().close()

    logger.warning("Bot was shutdown!")
