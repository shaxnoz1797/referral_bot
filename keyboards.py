from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    buttons = [
        [KeyboardButton(text="👤 Shaxsiy kabinet")],
        [KeyboardButton(text="🔗 Taklif qilish linki"), KeyboardButton(text="📊 Statistika")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard