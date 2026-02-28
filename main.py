import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, BotCommand
from aiogram.utils.keyboard import InlineKeyboardBuilder
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

user_languages = {}


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='start', description='Botni ishga tushirish 🔄'),
    ]
    await bot.set_my_commands(main_menu_commands)


@dp.message(CommandStart())
async def command_start(message: Message):
    ikb = InlineKeyboardBuilder()
    languages = [
        ('Rus 🇷🇺', 'ru'), ('Xitoy 🇨🇳', 'zh-TW'), ('Arab 🇸🇦', 'ar'),
        ('Hind 🇮🇳', 'hi'), ('Turk 🇹🇷', 'tr'), ('Ingliz 🇬🇧', 'en'),
        ('O‘zbek 🇺🇿', 'uz'), ('Qozoq 🇰🇿', 'kk'), ('Qirg‘iz 🇰🇬', 'ky'),
        ('Tojik 🇹🇯', 'tg'), ('Fransuz 🇫🇷', 'fr'), ('Nemis 🇩🇪', 'de'),
        ('Ispan 🇪🇸', 'es'), ('Italyan 🇮🇹', 'it'), ('Koreys 🇰🇷', 'ko'),
        ('Yapon 🇯🇵', 'ja'), ('Portugal 🇵🇹', 'pt'), ('Ukrain 🇺🇦', 'uk')
    ]

    for text, code in languages:
        ikb.add(InlineKeyboardButton(text=text, callback_data=f'lang_{code}'))

    ikb.adjust(2)
    await message.answer("Qaysi tilga tarjima qilamiz? / Choose target language:", reply_markup=ikb.as_markup())


@dp.callback_query(F.data.startswith('lang_'))
async def language_callback(callback: CallbackQuery):
    lang_code = callback.data.split('_')[1]
    user_languages[callback.from_user.id] = lang_code
    await callback.message.answer(f"Tanlandi! Endi matn yuboring, men uni tarjima qilaman.")
    await callback.answer()


@dp.message()
async def translate_message(message: Message):
    if not message.text:
        return

    user_id = message.from_user.id
    if user_id not in user_languages:
        await message.answer("Iltimos, avval /start buyrug'i orqali tilni tanlang!")
        return

    target_lang = user_languages[user_id]

    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(message.text)
        await message.answer(f"**Tarjima:**\n\n{translated}", parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Xatolik: {e}")
        await message.answer("Kechirasiz, tarjima qilishda xatolik yuz berdi.")


async def main():
    await set_main_menu(bot)

    await bot.delete_webhook(drop_pending_updates=True)

    print("Bot muvaffaqiyatli ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi")