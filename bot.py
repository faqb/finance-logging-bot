import asyncio
import asyncpg
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from asyncpg import Pool
from typing import Optional

from tgbot.config import Config
from tgbot.config import upload_admins
from tgbot.filters.role import RoleFilter, AdminFilter
from tgbot.handlers.admin.register import register_admin
from tgbot.handlers.user import register_user
from tgbot.middlewares.db import DbMiddleware
from tgbot.middlewares.lang import LangMiddleware
from tgbot.middlewares.locale import ACLMiddleware
from tgbot.middlewares.role import RoleMiddleware


logger = logging.getLogger(__name__)


async def create_pool(
        user: str,
        password: str,
        database: str,
        host: str
        ) -> Optional[Pool]:
    try:
        pool = await asyncpg.create_pool(
                user=user,
                password=password,
                database=database,
                host=host,
                command_timeout=1
                )
        return pool
    except ConnectionRefusedError as e:
        print(f"Caught this error: {repr(e)}")
        exit(1)


async def main() -> None:
    logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            )
    logger.info("Starting bot")
    config = Config()

    storage = MemoryStorage()
    pool = await create_pool(
            user=config.USER,
            password=config.PASSWORD,
            database=config.DATABASE,
            host=config.HOST,
            )

    # insert admins to database
    await upload_admins(pool, config.ADMINS)

    bot = Bot(token=config.TOKEN)
    dp = Dispatcher(bot, storage=storage)

    # load middlewares
    dp.middleware.setup(DbMiddleware(pool))
    dp.middleware.setup(RoleMiddleware(config.ADMINS))
    dp.middleware.setup(LangMiddleware())
    dp.middleware.setup(ACLMiddleware(config.I18N_DOMAIN, config.LOCALES_DIR))

    # load filters
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)

    # register handlers
    register_admin(dp)
    register_user(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
