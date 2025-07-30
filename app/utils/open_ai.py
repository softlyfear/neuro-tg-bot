"""Реализация взаимодействия с OpenAi с использованием HTTP proxy."""

import logging
import os

import httpx
from dotenv import load_dotenv
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)

load_dotenv("app/configs/.env")
proxy = os.getenv("PROXY_HTTP")
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    logger.error("Переменная окружения OPENAI_API_KEY не найдена в .env")
    raise ValueError("Переменная окружения OPENAI_API_KEY не найдена в .env")

# Подключение к open_ai через прокси
http_client = httpx.AsyncClient(
    proxy=proxy, transport=httpx.HTTPTransport(local_address="0.0.0.0")
)

client = AsyncOpenAI(api_key=api_key, http_client=http_client)


async def get_response_gpt(history: list[dict]) -> str:
    """Обработка запросов к чату GPT."""

    response = await client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=history
    )
    return response.choices[0].message.content
