from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile

import app.utils.keyboards as kb
from app.utils.open_ai import get_response_gpt
from app.utils.shared import BotState, cancel_flags, get_user_lock, get_history, user_histories

router  = Router()


# Обработчики команды "/recommendation" и кнопки "Рекомендации по фильмам и книгам"
@router.message(Command("recommendation"))
@router.message(F.text == "Рекомендации по фильмам и книгам")
async def start_recommendation_chat(message: Message, state: FSMContext):

    user_id = message.from_user.id
    user_histories.pop(user_id, None)
    cancel_flags.pop(user_id, None)

    await state.set_state(BotState.RECOMMENDATION)  # Задаем состояние RECOMMENDATION

    try:
        photo = FSInputFile("app/pictures/topic.jpeg")
        await message.answer_photo(photo=photo)
    except Exception as e:
        print(e)

    await message.answer("А также музыка =)", reply_markup=kb.main_menu_bottom)
    await message.answer(
        "Выберите тему для рекомендации: ", reply_markup=kb.recommendation_chat
    )


# Реагируем на кол беки в состоянии RECOMMENDATION
@router.callback_query(BotState.RECOMMENDATION, F.data.in_(["movies", "books", "music"]))
async def callback_recommendation(callback: CallbackQuery, state: FSMContext):
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


# Ловим сообщения от пользователя в состоянии RECOMMENDATION и отвечаем ему
@router.message(BotState.RECOMMENDATION)
async def recommendation(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lock = get_user_lock(user_id)  # создаем замок для пользователя

    if lock.locked():
        await message.answer("⏳ Подожди, запрос ещё обрабатывается...")
        return

    async with lock:
        if cancel_flags.get(user_id):  # Проверка отмены перед запросом
            return

        user_text = message.text
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
        history.append({"role": "assistant", "content": response})

        if cancel_flags.get(user_id):  # Проверка отмены после запроса
            return

        await message.answer(response, reply_markup=kb.recommendation_chat_menu)
