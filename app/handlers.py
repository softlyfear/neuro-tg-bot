from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from app.generators import gpt
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


router = Router()


class Generate(StatesGroup):
    text = State()


@router.message(CommandStart)
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Добро пожаловать в бота, напишите Ваш запрос!")


@router.message(F.text)
async def generate(message: Message, state: FSMContext):
    await message.answer("Подождите, ваше сообщение генерируется...")

    await state.set_state(Generate.text)
    try:
        response = await gpt(message.text)
        await message.answer(response.choices[0].message.content)
    except Exception as e:
        await message.answer(f"Ошибка при генерации ответа: {e}")

    await state.clear()
