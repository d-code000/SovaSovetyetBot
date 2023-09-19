import asyncio
import logging
import sys
import handlers

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

BOT_TOKEN = "BOT_TOKEN"


async def main() -> None:
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.include_router(handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
