from aiogram import Bot, Dispatcher, executor, types
import logging
import time
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from module import word
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from config import API_TOKEN, admin_id
import sqlite3
conn = sqlite3.connect('db.db', check_same_thread=False)
cursor = conn.cursor()
from reply_keyboard import keyboard1, keyboard2

def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
    cursor.execute('INSERT INTO test (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)',
                   (user_id, user_name, user_surname, username))
    conn.commit()

# logging.basicConfig(level=logging.DEBUG)


bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())


class File_send(StatesGroup):
    title = State()
    body = State()


@dp.message_handler(state='*',commands=['start'])
async def welcome(message: types.Message):
    await message.reply("""Assalomu alaykum botimizga xush kelibsiz. \nBu bot orqali siz Word file yaratishingiz mumkin.:)\n 
    word yaratish uchun /file""", reply_markup=keyboard1)
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    db_table_val(user_id=us_id, user_name=us_name,
                 user_surname=us_sname, username=username)

@dp.message_handler()
async def keyboard_answer(message: types.Message):
    if message.text == 'Word yaratish':
        await message.reply('Mavzuni kiriting', reply_markup=keyboard2)
        await File_send.title.set()
    elif message.text == 'Admin':
        await message.answer('Bot yaratuvchisi: @Ziyodulla')



@dp.message_handler(state=File_send.title)
async def filebody(message: types.Message, state=FSMContext):
    title = message.text
    if title == 'Bekor qilish':
        await message.reply("Qayta yaratish!", reply_markup=keyboard1)
        await state.reset_state(with_data=True)
    else:
        await state.update_data(title=title)
        await message.answer("Matn kiriting", reply_markup=keyboard2)
        await File_send.body.set()


@dp.message_handler(state=File_send.body)
async def filesend(message: types.Message, state: FSMContext):
    body = message.text
    if body == 'Bekor qilish':
        await message.reply("Qayta yaratish!", reply_markup=keyboard1)
        await state.reset_state(with_data=True)
    else:
        await state.update_data(body=body)
        data = await state.get_data()
        id = message.from_user.id
        file = word(data.get('title'), data.get('body'), id)
        await message.reply_document(open(file, 'rb'))
        await bot.send_document(admin_id, open(file, 'rb'))
        await bot.send_message(admin_id, message.from_user)
        os.remove(file)
        await state.reset_state(with_data=True)


if __name__ == '__main__':
    executor.start_polling(dp)
