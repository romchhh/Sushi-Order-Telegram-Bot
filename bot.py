import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import API_TOKEN, ADMIN_IDS, GROUP_ID
from user.user_functions import greet_user, get_item_price
from user.user_keyboard import create_menu_keyboard, create_about_keyboard, get_cart_keyboard, create_keyboard
from user.user_db import add_phone_number_to_user, add_name_to_user, save_order
from admin.admin_keyboard import admin_keyboard
from admin.admin_db import get_active_users_count, get_users_count, get_sales_count
from admin.admin_functions import export_database_to_excel
from menu.roles.rolls import menu as rolls
from menu.maki.maki import maki_menu as makis
from menu.sets.sets import menu_sets as sets
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await greet_user(message)

@dp.message_handler(lambda message: message.text == "Меню 📋")
async def process_menu_command(message: types.Message):
    await message.answer("Тут ви можете переглянути наше меню і зробити замовлення.", reply_markup=create_menu_keyboard())
    

class AddToCartStates(StatesGroup):
    item = State()
    quantity = State()
    user_id = State()
    
cart = {}

@dp.callback_query_handler(lambda query: query.data in ["roles", "sets", "maki"])
async def process_inline_callback(query: types.CallbackQuery):
    await query.answer()
    if query.data == "roles":
        photo_files = [
            "menu/roles/photos/philadelphia.jpg",
            "menu/roles/photos/philadelphia2.jpg",
            "menu/roles/photos/philadelphia3.jpg",
            "menu/roles/photos/california.jpg",
            "menu/roles/photos/california6.jpg",
            "menu/roles/photos/california3.jpg",
            "menu/roles/photos/california4.jpg"
        ]
        for i, roll in enumerate(rolls):
            roll_text = f"<b>{roll}</b>\n"
            roll_text += f"Інгредієнти: <i>{', '.join(rolls[roll]['ingredients'])}</i>\n"
            roll_text += f"Ціна: <b>{rolls[roll]['price']} грн</b>\n"
            roll_text += f"Вага: <b>{rolls[roll]['weight']} грам</b>\n"
            roll_text += f"Додатки: <i>{', '.join(rolls[roll]['accompaniments'])}</i>\n"
            with open(photo_files[i], "rb") as photo_file:
                message = await bot.send_photo(chat_id=query.message.chat.id, photo=photo_file, caption=roll_text, parse_mode='HTML')
                add_to_cart_button = types.InlineKeyboardButton(text="➕Додати в корзину", callback_data=f"add_to_cart:{roll}:1")
                inline_keyboard = types.InlineKeyboardMarkup().add(add_to_cart_button)
                await bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=message.message_id, reply_markup=inline_keyboard)
                
    if query.data == "sets":
        photo_files = [
            "menu/sets/photos/california.jpg",
            "menu/sets/photos/philadelphia.jpg",
            "menu/sets/photos/tokio.jpg"
        ]
        for i, menu_set in enumerate(sets):
            set_text = f"<b>{menu_set['name']}</b>\n"
            set_text += f"Ціна: <b>{menu_set['price']} грн</b>\n"
            set_text += f"Вага: <b>{menu_set['weight']} грам</b>\n"
            set_text += "Вміст: \n"

            for j, roll in enumerate(menu_set['contents']):
                set_text += f"{j + 1}. <b>{roll['name']}</b>\n"
                set_text += f"Інгредієнти: <i>{', '.join(roll['ingredients'])}</i>\n"
            set_text += f"Додатки: <i>{', '.join(menu_set['accompaniments'])}</i>\n"

            with open(photo_files[i], "rb") as photo_file:
                message = await bot.send_photo(chat_id=query.message.chat.id, photo=photo_file, caption=set_text, parse_mode='HTML')
                add_to_cart_button = types.InlineKeyboardButton(text="➕Додати в корзину", callback_data=f"add_to_cart:{menu_set['name']}:1")
                inline_keyboard = types.InlineKeyboardMarkup().add(add_to_cart_button)
                await bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=message.message_id, reply_markup=inline_keyboard)
                
    if query.data == "maki":
        photo_files = [
            "menu/maki/photos/makisalmon.jpg",
            "menu/maki/photos/makishrimpjpg.jpg",
            "menu/maki/photos/makieeljpg.jpg",
            "menu/maki/photos/makitunajpg.jpg",
            "menu/maki/photos/makicucumberjpg.jpg"
        ]
        for i, maki in enumerate(makis):
            maki_text = f"<b>{maki}</b>\n"
            maki_text += f"Інгредієнти: <i>{', '.join(makis[maki]['ingredients'])}</i>\n"
            maki_text += f"Ціна: <b>{makis[maki]['price']} грн</b>\n"
            maki_text += f"Вага: <b>{makis[maki]['weight']} грам</b>\n"
            with open(photo_files[i], "rb") as photo_file:
                message = await bot.send_photo(chat_id=query.message.chat.id, photo=photo_file, caption=maki_text, parse_mode='HTML')
                add_to_cart_button = types.InlineKeyboardButton(text="➕Додати в корзину", callback_data=f"add_to_cart:{maki}:1")
                inline_keyboard = types.InlineKeyboardMarkup().add(add_to_cart_button)
                await bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=message.message_id, reply_markup=inline_keyboard)

@dp.callback_query_handler(lambda query: query.data.startswith("add_to_cart"))
async def add_to_cart(query: types.CallbackQuery):
    user_id = query.from_user.id
    item_name, quantity = query.data.split(":")[1:]
    if user_id not in cart:
        cart[user_id] = {}
    if item_name not in cart[user_id]:
        cart[user_id][item_name] = int(quantity)
    else:
        cart[user_id][item_name] += int(quantity)
    remove_button = types.InlineKeyboardButton(text="-", callback_data=f"remove_from_cart:{item_name}:1")
    quantity_button = types.InlineKeyboardButton(text=f"{cart[user_id][item_name]} шт", callback_data=f"quantity:{item_name}:{cart[user_id][item_name]}")
    add_button = types.InlineKeyboardButton(text="+", callback_data=f"add_to_cart:{item_name}:1")
    view_cart_button = types.InlineKeyboardButton(text="Перейти в корзину", callback_data=f"view_cart:{user_id}")
    inline_keyboard = types.InlineKeyboardMarkup().add(remove_button, quantity_button, add_button, view_cart_button)

    await bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=inline_keyboard)
    print(f"Cart for user {user_id}: {cart[user_id]}")

@dp.callback_query_handler(lambda query: query.data.startswith("remove_from_cart"))
async def remove_from_cart(query: types.CallbackQuery):
    user_id = query.from_user.id
    item_name, quantity = query.data.split(":")[1:]
    if user_id not in cart:
        return
    if item_name not in cart[user_id]:
        return
    cart[user_id][item_name] -= int(quantity)
    if cart[user_id][item_name] <= 0:
        del cart[user_id][item_name]
        add_button = types.InlineKeyboardButton(text="➕Додати в корзину", callback_data=f"add_to_cart:{item_name}:1")
        inline_keyboard = types.InlineKeyboardMarkup().add(add_button)
    else:
        remove_button = types.InlineKeyboardButton(text="-", callback_data=f"remove_from_cart:{item_name}:1")
        quantity_button = types.InlineKeyboardButton(text=f"{cart[user_id][item_name]} шт", callback_data=f"quantity:{item_name}:{cart[user_id][item_name]}")
        add_button = types.InlineKeyboardButton(text="+", callback_data=f"add_to_cart:{item_name}:1")
        view_cart_button = types.InlineKeyboardButton(text="Перейти в корзину", callback_data=f"view_cart:{user_id}")
        inline_keyboard = types.InlineKeyboardMarkup().add(remove_button, quantity_button, add_button, view_cart_button)

    await bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=inline_keyboard)
    print(f"Cart for user {user_id}: {cart[user_id]}")


@dp.callback_query_handler(lambda query: query.data.startswith("view_cart"))
async def view_cart(query: types.CallbackQuery):
    user_id = int(query.data.split(":")[1])
    if user_id not in cart:
        await query.answer("Ваша корзина порожня.", show_alert=True)
        return

    cart_text = "<b>🗒 Чек</b>\n"
    cart_text += "--------------------------------------\n"
    cart_text += "<b>🍜 Ваше замовлення::</b>\n\n"

    total_price = 0
    for item_name, quantity in cart[user_id].items():
        item_price = get_item_price(item_name)
        if item_price is None:
            continue
        total_price += item_price * quantity
        if quantity > 1:
            cart_text += f"Назва: {item_name}\n"
            cart_text += f"Ціна: {quantity} x {item_price} грн. = {item_price * quantity} грн.\n\n"
        else:
            cart_text += f"Назва: {item_name}\n"
            cart_text += f"Ціна: {item_price} грн.\n\n"

    cart_text += "--------------------------------------\n"
    cart_text += f"<b>💸Сума:</b> {total_price} грн."

    inline_preview_keyboard = get_cart_keyboard(user_id)

    await bot.send_message(
        chat_id=query.from_user.id,
        text=cart_text,
        reply_markup=inline_preview_keyboard,
        parse_mode='HTML'
    )

class MyState(StatesGroup):
    phone_number_received = State()
    waiting_for_name = State()
    waiting_for_contact = State()  

phone_numbers = {}  # Словник для збереження номерів телефонів користувачів
names = {}  # Словник для збереження імен користувачів

def add_phone_number_to_user(user_id, phone_number):
    phone_numbers[user_id] = phone_number

def get_phone_number_from_user(user_id):
    return phone_numbers.get(user_id, None)

def add_name_to_user(user_id, name):
    names[user_id] = name

def get_name_from_user(user_id):
    return names.get(user_id, None)

@dp.callback_query_handler(lambda query: query.data.startswith("confirm_cart"))
async def confirm(query: types.CallbackQuery):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton('Надіслати номер телефону📞', request_contact=True))
    markup.add(types.KeyboardButton('🔙Назад'))

    await bot.send_message(query.message.chat.id, "Натисніть кнопку, щоб надіслати свій номер телефону:", reply_markup=markup)
    await MyState.phone_number_received.set()  # Change to phone_number_received

@dp.message_handler(content_types=['contact'], state=MyState.phone_number_received)
async def contact_received(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    user_id = message.from_user.id
    add_phone_number_to_user(user_id, phone_number)

    back_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back_markup.add(types.KeyboardButton('🔙Назад'))

    await message.reply("Будь ласка, введіть ваше ім'я:", reply_markup=back_markup)
    await MyState.waiting_for_name.set()

@dp.message_handler(state=MyState.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    if message.text == '🔙Назад':
        await back_to_menu_action(message, state)
        return

    user_real_name = message.text
    print(user_real_name)
    user_id = message.from_user.id
    add_name_to_user(user_id, user_real_name)

    user_phone_number = get_phone_number_from_user(user_id)
    user_cart = cart.get(user_id, {})

    order_message = f"<b>Нове замовлення:</b>\n\n"
    order_message += f"<b>Номер замовлення:</b> <code>{user_id}</code>\n"
    order_message += f"<b>Ім'я:</b> {user_real_name}\n"
    order_message += f"<b>Телефон:</b> <a href='tel:{user_phone_number}'>{user_phone_number}</a>\n"
    order_message += f"<b>Замовлення:</b>\n\n"

    total_price = 0
    items = ""
    for item_name, quantity in user_cart.items():
        item_price = get_item_price(item_name)
        if item_price is None:
            continue
        total_price += item_price * quantity
        if quantity > 1:
            order_message += f"{item_name}: {quantity} x {item_price} грн. = <b>{item_price * quantity} грн.</b>\n\n"
            items += f"{item_name}: {quantity} x {item_price} грн. = {item_price * quantity} грн.\n"
        else:
            order_message += f"{item_name}: <b>{item_price} грн.</b>\n"
            items += f"{item_name}: {item_price} грн.\n"

    order_message += f"\n<b>Сума:</b> <b>{total_price} грн.</b>"

    # Save order to database
    order_data = {
        'username': message.from_user.username,
        'real_name': user_real_name,
        'phone_number': user_phone_number,
        'items': items,
        'total_price': total_price
    }
    save_order(order_data)

    await bot.send_message(chat_id=GROUP_ID, text=order_message, parse_mode='HTML')

    keyboard = create_keyboard()
    if user_id in cart:
        del cart[user_id]
    await message.answer("Ваше замовлення обробляється. Скоро з вами зв'яжуться оператори.", reply_markup=keyboard)
    await state.finish()
    
async def back_to_menu_action(message: types.Message, state: FSMContext):
    try:
        keyboard = create_keyboard()
        await message.answer("Ви повернулись назад.", reply_markup=keyboard)
        await state.finish()
    except Exception as e:
        print(f"Error: {e}")
        
        
@dp.message_handler(lambda message: message.text == '🔙Назад', state='*')
async def back_to_menu_handler(message: types.Message, state: FSMContext):
    await back_to_menu_action(message, state)
        



def print_user_carts():
    for user_id, user_cart in cart.items():
        print(f"User {user_id} Cart:")
        for item_name, quantity in user_cart.items():
            print(f"Item: {item_name}, Quantity: {quantity}")


    
async def view_cart_callback(user_id):
    cart_text = "<b>🗒 Чек</b>\n"
    cart_text += "--------------------------------------\n"
    cart_text += "<b>🍜 Ваше замовлення::</b>\n\n"

    total_price = 0
    for item_name, quantity in cart[user_id].items():
        item_price = get_item_price(item_name)
        if item_price is None:
            continue
        total_price += item_price * quantity
        if quantity > 1:
            cart_text += f"Назва: {item_name}\n"
            cart_text += f"Ціна: {quantity} x {item_price} грн. = {item_price * quantity} грн.\n\n"
        else:
            cart_text += f"Назва: {item_name}\n"
            cart_text += f"Ціна: {item_price} грн.\n\n"

    cart_text += "--------------------------------------\n"
    cart_text += f"<b>💸Сума:</b> {total_price} грн."
    inline_preview_keyboard = get_cart_keyboard(user_id)
    await bot.send_message(chat_id=user_id, text=cart_text, reply_markup=inline_preview_keyboard, parse_mode='HTML')
      
@dp.callback_query_handler(lambda query: query.data.startswith("change_cart"))
async def change_cart(query: types.CallbackQuery):
    user_id = int(query.data.split(":")[1])
    if user_id not in cart:
        await query.answer("Ваша корзина порожня.", show_alert=True)
        return

    await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)

    keyboard = create_menu_keyboard()
    await bot.send_message(
        chat_id=query.message.chat.id,
        text="Оберіть ще щось з меню:",
        reply_markup=keyboard
    )

    
@dp.callback_query_handler(lambda query: query.data.startswith("cancel_cart"))
async def cancel_cart(query: types.CallbackQuery):
    user_id = int(query.data.split(":")[1])
    confirmation_text = "Ви впевнені, що хочете скасувати замовлення? Це очистить вашу корзину."
    confirmation_keyboard = types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton(text="Так", callback_data=f"confirm_cancel:{user_id}"),
        types.InlineKeyboardButton(text="Ні", callback_data="cancel_cancel")
    )
    await bot.send_message(chat_id=query.from_user.id, text=confirmation_text, reply_markup=confirmation_keyboard)


@dp.callback_query_handler(lambda query: query.data.startswith("confirm_cancel"))
async def confirm_cancel(query: types.CallbackQuery):
    user_id = int(query.data.split(":")[1])
    if user_id in cart:
        del cart[user_id]
    last_message_id = query.message.message_id
    previous_message_id = last_message_id - 1
    await bot.delete_message(chat_id=query.message.chat.id, message_id=last_message_id)
    await bot.delete_message(chat_id=query.message.chat.id, message_id=previous_message_id)
    await bot.send_message(chat_id=query.from_user.id, text="Ваше замовлення скасовано, і ваша корзина очищена.")
    
@dp.callback_query_handler(lambda query: query.data == "cancel_cancel")
async def cancel_cancel(query: types.CallbackQuery):
    last_message_id = query.message.message_id
    await bot.delete_message(chat_id=query.message.chat.id, message_id=last_message_id)


@dp.message_handler(lambda message: message.text == "Корзина 🛒")
async def process_order_command(message: types.Message):
    user_id = message.from_user.id
    if user_id not in cart:
        menu_keyboard = create_menu_keyboard() 
        await message.answer("Ваша корзина порожня, зробіть замовлення тут 🤗.", reply_markup=menu_keyboard)
        return
    await view_cart_callback(user_id)


@dp.message_handler(lambda message: message.text == "Про нас ℹ️")
async def process_about_command(message: types.Message):
    about_text = "🍣 Суші бар Самурай пропонує вам найсмачніші та найсвіжіші страви японської кухні. Завітайте до нас та насолоджуйтеся справжньою японською кухнею!"
    await message.answer(about_text, reply_markup=create_about_keyboard())
    

"""ADMIN"""
@dp.message_handler(commands=['admin'])
async def admin_panel(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if user_id in ADMIN_IDS:
        await bot.send_message(chat_id, "Ви увійшли до панелі адміністратора.", reply_markup=admin_keyboard)
        
@dp.message_handler(lambda message: message.text == 'Статистика 📊')
async def statistics_handler(message: types.Message):
    total_users = get_users_count()
    active_users = get_active_users_count()
    total_sales = get_sales_count()

    response_message = (
        f"👥 Загальна кількість користувачів: {total_users}\n"
        f"📱 Кількість активних користувачів: {active_users}\n"
        f"🛍️ Загальна кількість замовлень: {total_sales}"
    )
    await message.answer(response_message)

@dp.message_handler(lambda message: message.text == 'Вигрузити базу даних 💾')
async def export_database_handler(message: types.Message):
    await message.answer("Вигружаємо базу даних...")
    await export_database_to_excel(message)
    
        
@dp.message_handler(lambda message: message.text == 'Назад в меню ◀️')
async def back_to_menu_handler(message: types.Message):
    keyboard = create_keyboard()  # Викликаємо функцію create_keyboard()
    await message.answer("Ви повернулись назад.", reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)