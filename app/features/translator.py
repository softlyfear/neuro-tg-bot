"""
Роутер для режима переводчика на основе GPT.

Пользователь выбирает язык, GPT переводит вводимые сообщения на выбранный язык.

Список языков:
1. Русский
2. Английский
3. Японский
4. Немецкий
"""

import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile

import app.utils.keyboards as kb
from app.utils.open_ai import get_response_gpt
from app.utils.shared import BotState, cancel_flags, get_user_lock, get_history, user_histories

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("translate"))
@router.message(F.text == "Переводчик")
async def start_translator_chat(message: Message, state: FSMContext):
    """
    Обработка кнопок для входа в режим переводчика.

    - Удаление истории диалога
    - Сброс флага отмены
    """
    user_id = message.from_user.id
    user_histories.pop(user_id, None)
    cancel_flags.pop(user_id, None)

    await state.set_state(BotState.TRANSLATOR)

    try:
        photo = FSInputFile("app/pictures/translater.jpg")
        await message.answer_photo(photo=photo)
    except Exception as e:
        print(e)

    await message.answer(
        "Список доступных языков: ", reply_markup=kb.main_menu_bottom
    )
    await message.answer(
        "Перевод будет осуществлен с помощью GPT",
        reply_markup=kb.translate_chat,
    )


@router.callback_query(BotState.TRANSLATOR, F.data.in_(["russian", "english", "japan", "german"]))
async def start_new_chat(callback: CallbackQuery, state: FSMContext):
    """
    Обработка кнопок выбора языка.

    - Удаление истории диалога
    - Сброс флага отмены
    """
    user_id = callback.from_user.id
    select_language = callback.data

    user_histories.pop(user_id, None)
    cancel_flags.pop(user_id, None)

    await state.set_state(BotState.TRANSLATOR)
    await state.update_data(language=select_language)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(f"Вы выбрали язык {select_language}\n"
                                  f"Напишите текст для перевода",
                                  reply_markup=kb.main_menu_bottom)


@router.message(BotState.TRANSLATOR)
async def translater(message: Message, state: FSMContext):
    """
    Обработка и перевод на выбранный пользователем язык.

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
        logger.debug(f"User text message: {user_text}")
        history = get_history(user_id)

        data = await state.get_data()
        language = data.get("language")

        system_prompt = (
            f"Пользователь выбрал язык {language}, тебе нужно любые его сообщения переводить на {language}"
        )

        history.append({"role": "system", "content": system_prompt})
        history.append({"role": "user", "content": user_text})

        await message.chat.do("typing")

        response = await get_response_gpt(history)
        logger.debug(f"GPT answer: {response}")
        history.append({"role": "assistant", "content": response})

        if cancel_flags.get(user_id):
            return

        await message.answer(response, reply_markup=kb.main_menu_bottom)
