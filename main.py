import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F  # F qo'shildi
from aiogram.filters import Command, CommandObject
from dotenv import load_dotenv
from database import Database
from keyboards import main_menu  # Tugmalarni chaqiramiz

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
db = Database()


@dp.message(Command("start"))
async def start_command(message: types.Message, command: CommandObject):
    telegram_id = message.from_user.id
    full_name = message.from_user.full_name

    args = command.args
    referrer_id = None

    if args and args.isdigit():
        referrer_id = int(args)
        if referrer_id == telegram_id:
            referrer_id = None

    if not db.user_exists(telegram_id):
        db.add_user(telegram_id, full_name, referrer_id)
        if referrer_id:
            db.increment_referral(referrer_id)
            try:
                await bot.send_message(referrer_id, f"🎁 Yangi do'st qo'shildi: {full_name}")
            except:
                pass
        await message.answer(f"Xush kelibsiz! Botdan foydalanish uchun menyuni tanlang.", reply_markup=main_menu())
    else:
        await message.answer(f"Siz yana qaytganingizdan xursandmiz!", reply_markup=main_menu())


# Shaxsiy kabinet tugmasi bosilganda
@dp.message(F.text == "👤 Shaxsiy kabinet")
async def profile_handler(message: types.Message):
    count = db.get_referral_count(message.from_user.id)
    text = (f"👤 **Ismingiz:** {message.from_user.full_name}\n"
            f"🆔 **ID:** `{message.from_user.id}`\n"
            f"👥 **Taklif qilgan do'stlaringiz:** {count} ta")
    await message.answer(text, parse_mode="Markdown")


# Link olish tugmasi bosilganda
@dp.message(F.text == "🔗 Taklif qilish linki")
async def link_handler(message: types.Message):
    bot_info = await bot.get_me()
    link = f"https://t.me/{bot_info.username}?start={message.from_user.id}"
    await message.answer(f"Sizning referral linkingiz:\n\n{link}\n\nDo'stlaringizga yuboring va ball to'plang!")


# Statistika tugmasi (shunchaki qo'shimcha)
@dp.message(F.text == "📊 Statistika")
async def stats_handler(message: types.Message):
    await message.answer("Tez kunda umumiy statistika qo'shiladi...")


async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi.")