"""
Роутер для режима диалог с известной личностью.

Реализация, где GPT берет на себя роль выбранной пользователем личности и общается с ним в манере,
стиле и мировоззрении этой личности.

Список личностей:
1. Лев Толстой
2. Альберт Эйнштейн
3. Клеопатра
4. Стив Джобс
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


@router.message(Command("talk"))
@router.message(F.text.in_(["Диалог с известной личностью", "Начать новый диалог"]))
async def start_famous_person_chat(message: Message, state: FSMContext):
    """
    Обработка кнопок для входа в режим диалога и известной личностью.

    - Удаление истории диалога
    - Сброс флага отмены
    """
    user_id = message.from_user.id
    user_histories.pop(user_id, None)
    cancel_flags.pop(user_id, None)

    await state.set_state(BotState.TALK)

    try:
        photo = FSInputFile("app/pictures/persons.png")
        await message.answer_photo(photo=photo)
    except Exception as e:
        print(e)

    await message.answer(
        "Вы можете поговорить например на такие темы:", reply_markup=kb.main_menu_bottom
    )
    await message.answer(
        "Лев Толстой — мог бы говорить о философии, литературе\n"
        "\nАльберт Эйнштейн — мог бы обсуждать физику, теорию относительности\n"
        "\nКлеопатра — могла бы рассказать о древнем Египте\n"
        "\nСтив Джобс — мог бы поделиться идеями об инновациях и технологиях",
        reply_markup=kb.famous_chat,
    )


@router.callback_query(BotState.TALK, F.data.in_(["leo_tolstoy", "albert_einstein", "cleopatra", "steve_jobs"]))
async def start_new_chat(callback: CallbackQuery, state: FSMContext):
    """
    Обработка кнопок выбора личности.

    - Удаление истории диалога
    - Сброс флага отмены
    """
    user_id = callback.from_user.id
    selected_person = callback.data

    user_histories.pop(user_id, None)
    cancel_flags.pop(user_id, None)

    await state.set_state(BotState.TALK)
    await state.update_data(person=selected_person)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer("Приятного общения")
    await callback.message.answer(f"{callback.from_user.username} задай свой вопрос {selected_person}",
                                  reply_markup=kb.chat_gpt_finish_button)


@router.message(BotState.TALK)
async def chat_with_person(message: Message, state: FSMContext):
    """
    Выдача пользователю ответов в режиме выбранном им личности.

    - Блокировка новых запросов, если предыдущий еще обрабатывается
    - Сохранение истории диалога и поддержание контекста
    """
    user_id = message.from_user.id
    lock = get_user_lock(user_id)  # создаем замок для пользователя

    if lock.locked():
        await message.answer("⏳ Подожди, запрос ещё обрабатывается...")
        return

    async with lock:
        if cancel_flags.get(user_id):  # Проверка отмены перед запросом
            return

        user_text = message.text
        logger.debug(f"User text message: {user_text}")
        history = get_history(user_id)

        data = await state.get_data()
        person = data.get("person", "знаменитая личность")

        name = person.replace("_", " ").title()
        system_prompt = (
            f"Ты {name}. Общайся с пользователем и отвечай на его вопросы, "
            f"точно в манере, стиле и мировоззрении {name}, как если бы ты и был {name}."
        )

        history.append({"role": "system", "content": system_prompt})
        history.append({"role": "user", "content": user_text})

        await message.chat.do("typing")

        response = await get_response_gpt(history)
        logger.debug(f"GPT answer: {response}")
        history.append({"role": "assistant", "content": response})

        if cancel_flags.get(user_id):
            return

        await message.answer(response, reply_markup=kb.chat_gpt_finish_button)
