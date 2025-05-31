import os
import httpx
from dotenv import load_dotenv
from openai import AsyncOpenAI


load_dotenv()
proxy = os.getenv("PROXY_HTTP")
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("Переменная окружения OPENAI_API_KEY не найдена в .env")

http_client = httpx.AsyncClient(
    proxy=proxy,
    transport=httpx.HTTPTransport(local_address="0.0.0.0")
)

client = AsyncOpenAI(
    api_key=api_key,
    http_client=http_client
)


async def gpt(question: str):
    response = await client.chat.completions.create(
        messages=[{
            'role': 'user',
            'content': str(question)
        }],
        model="GPT-4o mini"
    )
    return response
