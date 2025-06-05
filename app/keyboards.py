from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Получить рандомный факт"), KeyboardButton(text="Задать вопрос gpt")],
        [KeyboardButton(text='Квиз'), KeyboardButton(text="Диалог с известной личностью")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню."
)


fact_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Хочу ещё факт"), KeyboardButton(text='Закончить')],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню."
)


chat_gpt_button = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Закончить', callback_data="finish_chatting")]]
)
