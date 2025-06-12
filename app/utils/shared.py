import asyncio

from aiogram.fsm.state import State, StatesGroup


# Присвоение состояний
class BotState(StatesGroup):
    FACT = State()
    QUIZ = State()
    TALK = State()
    GPT = State()
    TRANSLATER = State()
    RECOMMENDATION = State()


user_locks = {}  # Защита от спама
cancel_flags = {}  # Отмена вывода, если пользователь передумал
user_histories = {}  # Хранение переписки пользователя с gpt


# Асинхронная блокировка для указанного пользователя
def get_user_lock(user_id: int):
    if user_id not in user_locks:
        user_locks[user_id] = asyncio.Lock()
    return user_locks[user_id]


# Получение истории пользователя
def get_history(user_id: int):
    return user_histories.setdefault(user_id, [])
