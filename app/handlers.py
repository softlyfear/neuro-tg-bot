from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import app.keyboards as kb
from app.shared import cancel_flags, user_histories

router  = Router()


# Обработчик команды /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    await start_finish_command(message)


# Обработчик кнопки 'Закончить'
@router.message(F.text.in_(['Закончить', "Закончить диалог", "Выйти в главное меню"]))
async def finish_button(message: Message, state: FSMContext):
    user_id = message.from_user.id
    cancel_flags.pop(user_id, None)
    await state.clear()  # Сбросить текущее FSM состояние

    user_histories.pop(user_id, None)  # Удалить историю диалога

    await start_finish_command(message)


async def start_finish_command(message: Message):
    await message.answer(
        f"Вы в главном меню, {message.from_user.username}",
        reply_markup = kb.main_menu
    )
