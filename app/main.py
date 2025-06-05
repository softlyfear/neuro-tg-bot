import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.main_handlers import router as main_router
from app.random_fact import router as random_fact_router


async def main():
    load_dotenv()
    token = os.getenv("TELEGRAM_API_KEY")
    if not token:
        raise ValueError("Переменная окружения TELEGRAM_API_KEY не найдена в .env")

    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(main_router)
    dp.include_router(random_fact_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен!")
