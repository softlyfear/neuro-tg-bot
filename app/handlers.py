from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
import app.keyboards as kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Добро пожаловать в бота!", reply_markup=kb.main)


@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Это команда /help')
