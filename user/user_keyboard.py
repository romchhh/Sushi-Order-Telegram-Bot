from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types

def create_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons_row1 = [
        KeyboardButton(text="Меню 📋"),
        KeyboardButton(text="Корзина 🛒"),
    ]
    keyboard.add(*buttons_row1)
    buttons_row2 = [
        KeyboardButton(text="Про нас ℹ️"),
    ]
    keyboard.add(*buttons_row2)
    return keyboard


def create_menu_keyboard():
    keyboard = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton(text="Роли🍣", callback_data="roles"),
        InlineKeyboardButton(text="Сети🍱", callback_data="sets"),
        InlineKeyboardButton(text="Макі🇯🇵", callback_data="maki"),
    ]
    keyboard.add(*buttons)
    return keyboard


def get_cart_keyboard(user_id):
    confirm_button = types.InlineKeyboardButton(text="Підтвердити ✔️", callback_data=f"confirm_cart:{user_id}")
    cancel_button = types.InlineKeyboardButton(text="Відмінити ❌", callback_data=f"cancel_cart:{user_id}")
    edit_button = types.InlineKeyboardButton(text="Додати ще щось ➕", callback_data=f"change_cart:{user_id}")

    inline_preview_keyboard = types.InlineKeyboardMarkup(row_width=2)

    inline_preview_keyboard.add(confirm_button, cancel_button)
    inline_preview_keyboard.add(edit_button)
    
    return inline_preview_keyboard



def create_about_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    instagram_button = types.InlineKeyboardButton(text="Instagram", url="https://www.instagram.com/samurai_sushi_ck?igsh=MWpmYXNienJwcjRudA%3D%3D")
    google_reviews_button = types.InlineKeyboardButton(text="Google Відгуки", url="https://g.co/kgs/F3ABR1a")
    keyboard.add(instagram_button)
    keyboard.add(google_reviews_button)
    return keyboard




