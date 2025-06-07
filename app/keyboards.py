from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

# Главное меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Получить рандомный факт"), KeyboardButton(text="Задать вопрос gpt")],
        [KeyboardButton(text='Квиз(в разработке)'), KeyboardButton(text="Диалог с известной личностью")]
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

main_menu_bottom = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Выйти в главное меню")],
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


famous_chat = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Лев Толстой", callback_data="leo_tolstoy"),
                      InlineKeyboardButton(text="Альберт Эйнштейн", callback_data="albert_einstein")],
                     [InlineKeyboardButton(text="Клеопатра", callback_data='cleopatra'),
                      InlineKeyboardButton(text="Стив Джобс", callback_data="steve_jobs")],]
)
