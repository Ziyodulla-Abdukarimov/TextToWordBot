from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button1 = KeyboardButton('Word yaratish')
button2 = KeyboardButton('Admin')
button3 = KeyboardButton('Bekor qilish')

keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button1).add(button2)
keyboard2 = ReplyKeyboardMarkup(resize_keyboard=True).add(button3)