from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# async def for_answer():

#     builder = InlineKeyboardBuilder()

#     builder.row(*[
#         InlineKeyboardButton(text="Очистить сессию", callback_data="clear_session"),
#         InlineKeyboardButton(text="Поясни", callback_data="not_undestand"),
#         # InlineKeyboardButton(text="Перевести в голос (Beta)", callback_data="to_voice")
#     ],
#     width=2
#     )

#     return builder.as_markup()

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

async def for_answer():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Очистить сессию")], 
            # [KeyboardButton(text="Поясни")],
            # [KeyboardButton(text="Перевести в голос (Beta)")]  # Можно раскомментировать
        ],
        resize_keyboard=True  # Чтобы кнопки были компактнее
    )
    return keyboard

