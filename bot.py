from aiogram import Bot, Dispatcher, executor, types
import logging
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from module import word
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from config import API_TOKEN, admin_id
import sqlite3
conn = sqlite3.connect('db.db', check_same_thread=False)
cursor = conn.cursor()


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


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.reply("""Assalomu aleykum bo\'timizga xush kelibsiz. \nBu bot orqali siz Word file yaratishingiz mumkin.:)\n 
    word yaratish uchun /file""")
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    db_table_val(user_id=us_id, user_name=us_name,
                 user_surname=us_sname, username=username)


@dp.message_handler(commands='file', state="*")
async def fileinfo(message: types.Message):
    await message.answer('Mavzuni kiriting')
    await File_send.title.set()


@dp.message_handler(state=File_send.title)
async def filebody(message: types.Message, state=FSMContext):
    title = message.text
    await state.update_data(title=title)
    await message.answer("Matn kiriting")
    await File_send.body.set()


@dp.message_handler(state=File_send.body)
async def filesend(message: types.Message, state: FSMContext):
    body = message.text
    await state.update_data(body=body)
    data = await state.get_data()
    id = message.from_user.id
    file = word(data.get('title'), data.get('body'), id)
    await message.reply_document(open(file, 'rb'))
    os.remove(file)
    await state.reset_state(with_data=True)


if __name__ == '__main__':
    executor.start_polling(dp)
