import logging
import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from app.handlers import router


async def main():
    load_dotenv()

    token = os.getenv("TELEGRAM_API_KEY")
    if not token:
        raise ValueError("Переменная окружения TELEGRAM_API_KEY не найдена в .env")

    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен!")
