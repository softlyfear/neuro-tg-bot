from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton



main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Получить рандомный факт"), KeyboardButton(text="Задать вопрос gpt")],
    [KeyboardButton(text="Квиз"), KeyboardButton(text="Диалог с известной личностью")],
],
                        resize_keyboard=True,
                        input_field_placeholder="Выберите пункт меню.")


# settings = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='Example', url="example")]
# ])