
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
import os

API_TOKEN = '7312264371:AAGPwY8hCMkK__OdVp3dZ-vr0_s1rPk2WuM'
ADMIN_ID = '7312264371'  # Bu yerga o'zingizning admin Telegram user IDni qo'shing.

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

# Eslatma matni
async def send_welcome(message: types.Message):
    await message.reply(
        "Salom! Bu bot anonim xabarlarni yuborish imkonini beradi. Faqatgina sizga yuborilgan xabarlarni ko'rishingiz mumkin.
"
        "Admin bilan bog'lanish uchun /admin tuşmasini bosing.",
        parse_mode=ParseMode.MARKDOWN
    )

@dp.message_handler(commands=['start'])
async def send_start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("Admin bilan bog'lanish")
    markup.add(item)
    
    await message.answer(
        "Xush kelibsiz! Bu yerda anonim xabarlar yuborish mumkin. Quyidagi tugmani bosib, admin bilan bog'lanishingiz mumkin.",
        reply_markup=markup
    )

# Admin bilan bog'lanish uchun
@dp.message_handler(lambda message: message.text.lower() == "admin bilan bog'lanish")
async def admin_contact(message: types.Message):
    await message.answer(f"Siz admin bilan bog'lanishingiz mumkin: @{ADMIN_ID}")

# Anonim xabar yuborish
@dp.message_handler(lambda message: message.text)
async def anon_message(message: types.Message):
    if message.from_user.id != int(ADMIN_ID):
        # Adminni nazorat qilish
        await bot.send_message(ADMIN_ID, f"Yangi anonim xabar:
{message.text}")
        await message.reply("Sizning xabaringiz yuborildi, admin uni ko'radi.")
    else:
        await message.reply("Siz admin sifatida bu botda ishlayapsiz!")

# Admin monitoring (xabarlarni ko'rish)
@dp.message_handler(commands=['monitoring_on'])
async def monitoring_on(message: types.Message):
    if str(message.from_user.id) == ADMIN_ID:
        await message.reply("Admin, endi siz yuborilgan barcha xabarlarni ko'rishingiz mumkin.")
    else:
        await message.reply("Sizda bu huquq yo'q!")

@dp.message_handler(commands=['monitoring_off'])
async def monitoring_off(message: types.Message):
    if str(message.from_user.id) == ADMIN_ID:
        await message.reply("Monitoring to'xtatildi.")
    else:
        await message.reply("Sizda bu huquq yo'q!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
