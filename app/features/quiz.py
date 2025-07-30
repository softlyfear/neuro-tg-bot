"""
Роутер для режима квиз с помощью GPT.

Реализация, где GPT проводит квиз пользователю, на выбранную им тему и подсчитывает результат.

Список тем квиза:
1. Кино
2. Наука
3. Игры
"""

import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery

import app.utils.keyboards as kb
from app.utils.open_ai import get_response_gpt
from app.utils.shared import (
    BotState,
    cancel_flags,
    user_histories,
    get_user_lock,
    get_history,
)

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("quiz"))
@router.message(F.text == "Квиз")
async def start_famous_person_chat(message: Message, state: FSMContext):
    """
    Обработка кнопок для входа в режим квиз.

    - Удаление истории диалога
    - Сброс флага отмены
    """
    user_id = message.from_user.id
    user_histories.pop(user_id, None)
    cancel_flags.pop(user_id, None)

    await state.set_state(BotState.QUIZ)

    try:
        photo = FSInputFile("app/pictures/quiz.jpg")
        await message.answer_photo(photo=photo)
    except Exception as e:
        print(e)

    await message.answer(
        "Выберите тему квиза:", reply_markup=kb.main_menu_bottom
    )
    await message.answer(
        "История — древние цивилизации\n"
        "\nКино — фильмы и режиссура\n"
        "\nНаука — открытия и теории\n"
        "\nИгры — видеоигры и гейминг",
        reply_markup=kb.quiz_chat,
    )


@router.message(BotState.QUIZ, F.text == "Начать новый квиз")
async def start_new_chat(message: Message, state: FSMContext):
    """
    Обработка кнопки для нового квиза.

    - Удаление истории диалога
    - Сброс флага отмены
    """
    user_id = message.from_user.id
    user_histories.pop(user_id, None)
    cancel_flags.pop(user_id, None)

    await state.set_state(BotState.QUIZ)
    await message.answer("Выберите тему квиза:", reply_markup=kb.main_menu_bottom)
    await message.answer(
        "История — древние цивилизации\n"
        "\nКино — фильмы и режиссура\n"
        "\nНаука — открытия и теории\n"
        "\nИгры — видеоигры и гейминг",
        reply_markup=kb.quiz_chat,
    )


@router.callback_query(BotState.QUIZ, F.data.in_(["history", "movie", "science", "games"]))
async def start_new_chat(callback: CallbackQuery, state: FSMContext):
    """
    Выдача вопросов пользователю на заданную им тему.

    - Блокировка новых запросов, если предыдущий еще обрабатывается
    - Сохранение истории диалога и поддержание контекста
    """
    user_id = callback.from_user.id
    selected_quiz = callback.data

    user_histories.pop(user_id, None)
    cancel_flags.pop(user_id, None)

    await state.set_state(BotState.QUIZ)
    await state.update_data(quiz=selected_quiz)
    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.message.answer("Тогда начнем!", reply_markup=kb.quiz_finish_button)

    lock = get_user_lock(user_id)

    async with lock:

        if cancel_flags.get(user_id):
            return

        history = get_history(user_id)

        system_prompt = (
            f"У пользователя выбрана тема '{selected_quiz}'. "
            f"Задавай вопрос под нумерацией (например, 1.), жди ответа в виде цифры. "
            f"После ответа говори, правильно или нет, и сразу задавай следующий вопрос. "
            f"Считай правильные и неправильные ответы и выводи в конце сообщения"
        )

        history.append({"role": "system", "content": system_prompt})

        await callback.message.chat.do("typing")
        response = await get_response_gpt(history)
        history.append({"role": "assistant", "content": response})

        if cancel_flags.get(user_id):
            return

        await callback.message.answer(response, reply_markup=kb.quiz_finish_button)


@router.message(BotState.QUIZ)
async def quiz(message: Message, state: FSMContext):
    """
    Выдача новых вопросов пользователю на заданную им тему.

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

        history.append({"role": "user", "content": user_text})

        await message.chat.do("typing")

        response = await get_response_gpt(history)
        logger.debug(f"GPT answer: {response}")
        history.append({"role": "assistant", "content": response})

        if cancel_flags.get(user_id):
            return

        await message.answer(response, reply_markup=kb.quiz_finish_button)
