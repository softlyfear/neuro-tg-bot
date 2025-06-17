"""Роутер для обработки выхода в главное меню."""

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import app.utils.keyboards as kb
from app.utils.shared import cancel_flags, user_histories

router  = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Обработчик команды /start."""
    await start_finish_command(message)


@router.message(F.text.in_(["Закончить", "Закончить диалог", "Выйти в главное меню"]))
async def finish_button(message: Message, state: FSMContext):
    """
    Обработка кнопок выхода в главное меню.

    - Отмена ожидающих ответов
    - Сброс текущих FSM состояний
    - Удаление истории диалога
    """
    user_id = message.from_user.id
    cancel_flags[user_id] = True

    await state.clear()
    user_histories.pop(user_id, None)

    await start_finish_command(message)


async def start_finish_command(message: Message):
    """Переход в главное меню."""
    await message.answer(
        f"Вы в главном меню, {message.from_user.username}",
        reply_markup = kb.main_menu
    )
