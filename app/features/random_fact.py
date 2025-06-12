from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

import app.utils.keyboards as kb
from app.utils.open_ai import get_response_gpt
from app.utils.shared import (
    BotState,
    cancel_flags,
    get_user_lock,
    get_history,
)

router  = Router()


# Обработчик команды /random и кнопки "Получить рандомный факт"
@router.message(F.text == "Получить рандомный факт")
@router.message(Command("random"))
async def get_random(message: Message, state: FSMContext):

    try:
        photo = FSInputFile("pictures/did-you-know-icon.jpg")
        await message.answer_photo(photo=photo)
    except Exception as e:
        print(e)

    await random_command(message, state)


# Обработчик кнопки "Хочу ещё факт", тут уже не будет повторно вставляться картинка
@router.message(F.text == "Хочу ещё факт")
async def get_random2(message: Message, state: FSMContext):
    await random_command(message, state)


# Запрос к open_ai на генерацию факта
async def random_command(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lock = get_user_lock(user_id)

    system_prompt = ("Напиши любой рандомный факт, максимально интересный, не повторяйся!")

    if lock.locked():
        await message.answer("⏳ Подожди, запрос ещё обрабатывается...")
        return

    async with lock:
        await state.set_state(BotState.FACT)
        await message.answer("Генерирую факт...", reply_markup=kb.fact_menu)

        history = get_history(user_id)
        history.append({"role": "system", "content": system_prompt})

        await message.chat.do("typing")

        response = await get_response_gpt(history)
        history.append({"role": "assistant", "content": response})

        if cancel_flags.get(user_id):
            return

        await message.answer(response)
