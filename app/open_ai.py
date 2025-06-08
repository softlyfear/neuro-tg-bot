import os

import httpx
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()
proxy = os.getenv("PROXY_HTTP")
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("Переменная окружения OPENAI_API_KEY не найдена в .env")

# Подключение к open_ai через прокси
http_client = httpx.AsyncClient(
    proxy=proxy, transport=httpx.HTTPTransport(local_address="0.0.0.0")
)

client = AsyncOpenAI(api_key=api_key, http_client=http_client)


# Обработка запроса на случайный факт
async def get_random_gpt():
    response = await client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[{"role": "user", "content": "Напиши любой рандомный факт"}],
    )
    return response.choices[0].message.content


# Диалог с gpt
async def get_response_gpt(history: list[dict]) -> str:
    response = await client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=history
    )
    return response.choices[0].message.content


# Диалог с известной личностью
async def get_response_person(history: list[dict]) -> str:
    response = await client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=history
    )
    return response.choices[0].message.content


# Квиз запросы
async def get_response_quiz(history: list[dict]) -> str:
    response = await client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=history
    )
    return response.choices[0].message.content
