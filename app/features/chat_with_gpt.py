"""Роутер с реализацией стандартного GPT интерфейса вопрос/ответ с сохранением контекста диалога"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

import app.utils.keyboards as kb
from app.utils.open_ai import get_response_gpt
from app.utils.shared import (
    get_user_lock,
    BotState,
    cancel_flags,
    get_history,
    user_histories,
)

router = Router()


@router.message(Command("gpt"))
@router.message(F.text == "Задать вопрос gpt")
async def start_gpt_chat(message: Message, state: FSMContext):
    """
    Обработка кнопок для входа в режим работы с GPT.

    - Удаление истории диалога
    - Сброс флага отмены
    """

    user_id = message.from_user.id
    user_histories.pop(user_id, None)
    cancel_flags.pop(user_id, None)
    await state.set_state(BotState.GPT)

    try:
        photo = FSInputFile("app/pictures/chatgpt.jpg")
        await message.answer_photo(photo=photo)
    except Exception as e:
        print(e)

    await message.answer(
        "Вы начали диалог с GPT!\nНапишите свой вопрос!",
        reply_markup=kb.chat_gpt_finish_button,
    )


@router.message(BotState.GPT, F.text == "Начать новый диалог")
async def start_new_chat(message: Message, state: FSMContext):
    """
    Обработка кнопки для входа в новый диалог.

    - Удаление истории диалога
    - Сброс флага отмены
    """
    user_id = message.from_user.id
    user_histories.pop(user_id, None)
    cancel_flags.pop(user_id, None)
    await state.set_state(BotState.GPT)
    await message.answer(
        "Вы начали новый диалог с GPT!\nНапишите свой вопрос!",
        reply_markup=kb.chat_gpt_finish_button,
    )


@router.message(BotState.GPT)
async def chat_with_gpt(message: Message):
    """
    Выдача ответа пользователю на заданные им вопросы к GPT.

    - Блокировка новых запросов, если предыдущий еще обрабатывается
    - Сохранение истории диалога и поддержание контекста
    """
    user_id = message.from_user.id
    lock = get_user_lock(user_id)

    if lock.locked():
        await message.answer("⏳ Подожди, запрос ещё обрабатывается...")
        return

    async with lock:
        if cancel_flags.get(user_id):
            return

        user_text = message.text
        history = get_history(user_id)
        history.append({"role": "user", "content": user_text})

        await message.chat.do("typing")

        response = await get_response_gpt(history)
        history.append({"role": "assistant", "content": response})

        if cancel_flags.get(user_id):
            return

        await message.answer(response, reply_markup=kb.chat_gpt_finish_button)
