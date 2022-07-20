from aiogram import Bot, Dispatcher, executor, types
import logging
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from module import word
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

logging.basicConfig(level=logging.DEBUG)

API_TOKEN = '5403184577:AAFG_LLYYx7sDdKpp61fhSVhR7fEW7hqaGY'

bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot, storage=MemoryStorage())

class File_send(StatesGroup):
    title = State()
    body =  State()

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.reply("""Assalomu aleykum bo\'timizga xush kelibsiz. \nBu bot orqali siz Word file yaratishingiz mumkin.:)\n 
    word yaratish uchun /file
    """)

@dp.message_handler(commands = 'file', state="*")
async def fileinfo(message: types.Message):
    await message.answer('Mavzuni kiriting')
    await File_send.title.set()

@dp.message_handler(state=File_send.title)
async def filebody(message : types.Message, state = FSMContext):
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