import os
import sqlite3
from openpyxl import Workbook
from aiogram import types

def export_table_to_excel(table_name, file_name):
    conn = sqlite3.connect("data/data.db")
    c = conn.cursor()

    c.execute(f"SELECT * FROM {table_name}")
    rows = c.fetchall()

    wb = Workbook()
    ws = wb.active

    c.execute(f"PRAGMA table_info({table_name})")
    column_names = [column[1] for column in c.fetchall()]

    ws.append(column_names)

    for row in rows:
        ws.append(row)

    wb.save(file_name)

async def export_database_to_excel(message: types.Message):
    export_table_to_excel("users", "users_database.xlsx")

    export_table_to_excel("orders", "orders_database.xlsx")

    await message.answer_document(document=open("users_database.xlsx", "rb"), caption="Таблиця з користувачами експортована")
    await message.answer_document(document=open("orders_database.xlsx", "rb"), caption="Таблиця з замовленнями експортована")

    os.remove("users_database.xlsx")
    os.remove("orders_database.xlsx")