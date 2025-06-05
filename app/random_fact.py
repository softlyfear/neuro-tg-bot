from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import app.keyboards as kb
from app.open_ai import get_random_gpt
from shared import cancel_flags, BotState
from shared import get_user_lock

router  = Router()


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

        fact = await get_random_gpt()
        if cancel_flags.get(user_id):  # Проверка отмены после запроса
            return

        await message.answer(fact)


# Обработчик команды /random
@router.message(Command('random'))
async def get_random(message: Message, state: FSMContext):
    await random_command(message, state)


# Обработчик кнопки "Получить рандомный факт" и "Хочу ещё факт"
@router.message(F.text.in_(["Получить рандомный факт", "Хочу ещё факт"]))
async def get_fact_button(message: Message, state: FSMContext):
    await random_command(message, state)
