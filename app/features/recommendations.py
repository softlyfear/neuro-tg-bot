"""
Роутер для режима рекомендации с помощью GPT.

Реализация, где пользователь выбирает тему для рекомендаций, после пишет жанр.
GPT дает список рекомендаций, а также присылает новый, если список не понравился.

Список тем:
1. История
2. Кино
3. Наука
4. Игры
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


@router.message(Command("recommendation"))
@router.message(F.text == "Рекомендации по фильмам и книгам")
async def start_recommendation_chat(message: Message, state: FSMContext):
    """
    Обработка кнопок для входа в режим рекомендаций.

    - Удаление истории диалога
    - Сброс флага отмены
    """
    user_id = message.from_user.id
    user_histories.pop(user_id, None)
    cancel_flags.pop(user_id, None)

    await state.set_state(BotState.RECOMMENDATION)

    try:
        photo = FSInputFile("app/pictures/topic.jpeg")
        await message.answer_photo(photo=photo)
    except Exception as e:
        print(e)

    await message.answer("А также музыка =)", reply_markup=kb.main_menu_bottom)
    await message.answer(
        "Выберите тему для рекомендации: ", reply_markup=kb.recommendation_chat
    )


@router.callback_query(BotState.RECOMMENDATION, F.data.in_(["movies", "books", "music"]))
async def callback_recommendation(callback: CallbackQuery, state: FSMContext):
    """
    Обработка кнопок выбора темы.

    - Удаление истории диалога
    - Сброс флага отмены
    """
    user_id = callback.from_user.id
    select_topic = callback.data

    user_histories.pop(user_id, None)
    cancel_flags.pop(user_id, None)

    await state.set_state(BotState.RECOMMENDATION)

    await state.update_data(topic=select_topic)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(f"Вы выбрали тему {select_topic}\n"
                                  f"Напишите желаемый жанр",
                                  reply_markup=kb.main_menu_bottom)


@router.message(BotState.RECOMMENDATION)
async def recommendation(message: Message, state: FSMContext):
    """
    Выдача рекомендаций пользователю на заданную им тему.

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
        topic = data.get("topic")

        system_prompt = (
            f"Пользователь выбрал тему для рекомендаций {topic}, тебе нужно подбирать рекомендации на написанный им жанр"
            f"Если пользователь написал Не нравится, ты даешь новый ответ, учитывая все неинтересные произведения"
            f"Не задавай лишних вопросов, сразу пиши новые рекомендации"
        )

        history.append({"role": "system", "content": system_prompt})
        history.append({"role": "user", "content": user_text})

        await message.chat.do("typing")

        response = await get_response_gpt(history)
        logger.debug(f"GPT answer: {response}")
        history.append({"role": "assistant", "content": response})

        if cancel_flags.get(user_id):
            return

        await message.answer(response, reply_markup=kb.recommendation_chat_menu)
