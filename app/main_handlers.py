from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import app.keyboards as kb
from shared import cancel_flags

router  = Router()


async def start_finish_command(message: Message):
    await message.answer(
        f"Вы в главном меню, {message.from_user.username}"
        f"\nВот список доступных команд:"
        f"\n\n/random - получить рандомный факт"
        f"\n/gpt - задать вопрос gpt"
        f"\n/talk - диалог с известной личностью"
        f"\n/quiz - квиз на выбранную тему",
        reply_markup = kb.main_menu
    )


# Обработчик команды /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    await start_finish_command(message)


# Обработчик кнопки 'Закончить'
@router.message(F.text == 'Закончить')
async def finish_button(message: Message, state: FSMContext):
    user_id = message.from_user.id
    cancel_flags[user_id] = True
    await state.clear()  # Сбросить текущее FSM состояние
    await start_finish_command(message)
