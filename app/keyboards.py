from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

# Главное меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Получить рандомный факт"), KeyboardButton(text="Задать вопрос gpt")],
        [KeyboardButton(text='Квиз(в разработке)'), KeyboardButton(text="Диалог с известной личностью(в разработке)")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню"
)

# Меню фактов
fact_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Хочу ещё факт"), KeyboardButton(text='Закончить')],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню"
)

# Кнопка закончить диалог с gpt
chat_gpt_finish_button = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Закончить диалог"), KeyboardButton(text="Начать новый диалог")]],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню"
)
