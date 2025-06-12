import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.features.chat_with_gpt import router as gpt_router
from app.features.famous_person import router as famous_person_router
from app.features.quiz import router as quiz_router
from app.features.random_fact import router as random_fact_router
from app.features.translator import router as translater
from app.utils.common_handlers import router as main_router


async def main():
    load_dotenv()
    token = os.getenv("TELEGRAM_API_KEY")
    if not token:
        raise ValueError("Переменная окружения TELEGRAM_API_KEY не найдена в .env")

    bot = Bot(token=token)  # Работа с api telegram
    dp = Dispatcher()  # Создаем диспетчер

    # Подключаем роутеры к диспетчеру
    dp.include_router(main_router)
    dp.include_router(random_fact_router)
    dp.include_router(gpt_router)
    dp.include_router(famous_person_router)
    dp.include_router(quiz_router)
    dp.include_router(translater)

    await dp.start_polling(bot)  # Пулим бота


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен!")
