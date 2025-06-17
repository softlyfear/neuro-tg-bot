"""Вспомогательные утилиты."""

import asyncio

from aiogram.fsm.state import State, StatesGroup


class BotState(StatesGroup):
    """
    Группа состояний для различных режимов работы бота.
    """
    FACT = State()
    QUIZ = State()
    TALK = State()
    GPT = State()
    TRANSLATER = State()
    RECOMMENDATION = State()


user_locks = {}  # Защита от спама
cancel_flags = {}  # Отмена вывода, если пользователь передумал
user_histories = {}  # Хранение переписки пользователя с gpt


def get_user_lock(user_id: int):
    """Асинхронная блокировка для указанного пользователя."""
    if user_id not in user_locks:
        user_locks[user_id] = asyncio.Lock()
    return user_locks[user_id]


def get_history(user_id: int):
    """Получение истории пользователя."""
    return user_histories.setdefault(user_id, [])
