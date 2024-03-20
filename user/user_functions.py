from aiogram import types
from user.user_keyboard import create_keyboard
from user.user_db import create_table, add_user
from aiogram import types
from menu.roles.rolls import menu as rolls
from menu.maki.maki import maki_menu as makis
from menu.sets.sets import menu_sets as sets

async def greet_user(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    user_first_name = message.from_user.first_name
    create_table()
    add_user(user_id, user_name, user_first_name)
    await message.answer(f"Привіт, {user_first_name}!")

    keyboard = create_keyboard()
    await message.answer("Виберіть опцію:", reply_markup=keyboard)
    
    
def get_item_price(item_name):
    if item_name in rolls:
        return rolls[item_name]["price"]

    if item_name in makis:
        return makis[item_name]["price"]

    for menu_set in sets:
        if menu_set["name"] == item_name:
            return menu_set["price"]
    return None
    
