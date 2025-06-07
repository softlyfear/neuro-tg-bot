from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import app.keyboards as kb
from app.open_ai import get_response_person
from app.shared import BotState, cancel_flags, get_user_lock, get_history, user_histories

router  = Router()


@router.message(Command("talk"))
@router.message(F.text.in_(["Диалог с известной личностью", 'Начать новый диалог']) )
async def start_famous_person_chat(message: Message, state: FSMContext):

    user_id = message.from_user.id
    user_histories.pop(user_id, None)
    cancel_flags.pop(user_id, None)

    await state.set_state(BotState.TALK)
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


@router.callback_query(BotState.TALK, F.data.in_(["leo_tolstoy", "albert_einstein", 'cleopatra', "steve_jobs"]))
async def start_new_chat(callback: CallbackQuery, state: FSMContext):
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

        response = await get_response_person(history)
        history.append({"role": "assistant", "content": response})

        if cancel_flags.get(user_id):  # Проверка отмены после запроса
            return

        await message.answer(response, reply_markup=kb.chat_gpt_finish_button)
