import asyncio

from aiogram.fsm.state import State, StatesGroup


class BotState(StatesGroup):
    FACT = State()
    QUIZ = State()
    TALK = State()
    GPT = State()


user_locks = {}  # защита от спама
cancel_flags = {}  #  отмена вывода, если пользователь передумал


def get_user_lock(user_id: int):
    if user_id not in user_locks:
        user_locks[user_id] = asyncio.Lock()
    return user_locks[user_id]
