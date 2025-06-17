"""Основной модуль для запуска neuro-tg-bot."""

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.features.chat_with_gpt import router as gpt_router
from app.features.famous_person import router as famous_person_router
from app.features.quiz import router as quiz_router
from app.features.random_fact import router as random_fact_router
from app.features.recommendations import router as recommendation_router
from app.features.translator import router as translater_router
from app.utils.common_handlers import router as common_handlers_router


async def main():
    """
    Инициализация и запуск Telegram-бота.

    - Загружает .env переменные
    - Создает экземпляры Bot и Dispatcher
    - Регистрирует роутеры
    - Запускает long polling
    """
    load_dotenv()
    token = os.getenv("TELEGRAM_API_KEY")
    if not token:
        raise ValueError("Переменная окружения TELEGRAM_API_KEY не найдена в .env")

    bot = Bot(token=token)
    dp = Dispatcher()

    dp.include_router(common_handlers_router)
    dp.include_router(random_fact_router)
    dp.include_router(gpt_router)
    dp.include_router(famous_person_router)
    dp.include_router(quiz_router)
    dp.include_router(translater_router)
    dp.include_router(recommendation_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен!")
