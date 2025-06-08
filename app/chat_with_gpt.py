from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

import app.keyboards as kb
from app.open_ai import get_response_gpt
from app.shared import (
    get_user_lock,
    BotState,
    cancel_flags,
    get_history,
    user_histories,
)

router  = Router()


# Обработчики команды "/gpt" и кнопки "Задать вопрос gpt"
@router.message(Command("gpt"))
@router.message(F.text == "Задать вопрос gpt")
async def start_gpt_chat(message: Message, state: FSMContext):
    await state.set_state(BotState.GPT)

    try:
        photo = FSInputFile("pictures/chatgpt.jpg")
        await message.answer_photo(photo=photo)
    except Exception as e:
        print(e)

    await message.answer(
        "Вы начали диалог с GPT!\nНапишите свой вопрос!",
        reply_markup=kb.chat_gpt_finish_button,
    )


# Обработчик кнопки "Начать новый диалог"
@router.message(BotState.GPT, F.text == "Начать новый диалог")
async def start_new_chat(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_histories.pop(user_id, None)
    cancel_flags.pop(user_id, None)
    await state.set_state(BotState.GPT)
    await message.answer(
        "Вы начали новый диалог с GPT!\nНапишите свой вопрос!",
        reply_markup=kb.chat_gpt_finish_button,
    )


# Ловим сообщения от пользователя в состоянии GPT и отвечаем ему
@router.message(BotState.GPT)
async def chat_with_gpt(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lock = get_user_lock(user_id)

    if lock.locked():
        await message.answer("⏳ Подожди, запрос ещё обрабатывается...")
        return

    async with lock:
        if cancel_flags.get(user_id):  # Проверка отмены перед запросом
            return

        user_text = message.text
        history = get_history(user_id)
        history.append({"role": "user", "content": user_text})

        await message.chat.do("typing")

        response = await get_response_gpt(history)
        history.append({"role": "assistant", "content": response})

        if cancel_flags.get(user_id):  # Проверка отмены после запроса
            return

        await message.answer(response, reply_markup=kb.chat_gpt_finish_button)
