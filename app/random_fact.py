from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

import app.keyboards as kb
from app.open_ai import get_random_gpt
from app.shared import get_user_lock, BotState, cancel_flags

router  = Router()


# Обработчик команды /random и кнопок "Получить рандомный факт" и "Хочу ещё факт"
@router.message(F.text == "Получить рандомный факт")
@router.message(Command('random'))
async def get_random(message: Message, state: FSMContext):

    try:
        photo = FSInputFile("pictures/did-you-know-icon.jpg")
        await message.answer_photo(photo=photo)
    except Exception as e:
        print(e)

    await random_command(message, state)


@router.message(F.text == "Хочу ещё факт")
async def get_random2(message: Message, state: FSMContext):
    await random_command(message, state)


# Обработка функционала random
async def random_command(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lock = get_user_lock(user_id)

    if lock.locked():
        await message.answer("⏳ Подожди, запрос ещё обрабатывается...")
        return

    async with lock:
        await state.set_state(BotState.FACT)
        await message.answer("Генерирую факт...", reply_markup=kb.fact_menu)

        if cancel_flags.get(user_id):  # Проверка отмены перед запросом
            return
        
        await message.chat.do("typing")
        fact = await get_random_gpt()
        if cancel_flags.get(user_id):  # Проверка отмены после запроса
            return

        await message.answer(fact)
