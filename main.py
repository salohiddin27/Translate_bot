import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, BotCommand
from aiogram.utils.keyboard import InlineKeyboardBuilder
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

user_languages = {}


class BotState(StatesGroup):
    waiting_for_example = State()


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='start', description='Botni ishga tushirish 🔄'),
    ]
    await bot.set_my_commands(main_menu_commands)


@dp.message(CommandStart())
async def commands_start(message: Message, state: FSMContext):
    await state.clear()
    ikb = InlineKeyboardBuilder()
    ikb.row(
        InlineKeyboardButton(text="Calculator 🔢", callback_data="calcula_"),
        InlineKeyboardButton(text="Languages 🇺🇿", callback_data="language_"),
    )
    ikb.adjust(2)
    await message.answer("O'zizga kerakli tugmani tanlang!", reply_markup=ikb.as_markup())


@dp.callback_query(F.data == 'calcula_')
async def start_calc(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BotState.waiting_for_example)
    await callback.message.answer("📊 Kalkulyator rejimi yoqildi.\n\nMisolni yozing (masalan: 80+10*(55/11)):")
    await callback.answer()


@dp.message(BotState.waiting_for_example)
async def calculate_math(message: Message, state: FSMContext):
    expression = message.text
    allowed = "0123456789+-*/(). "
    if not all(c in allowed for c in expression):
        await message.answer("❌ Xato! Faqat raqamlar va matematik amallarni yozing.")
        return

    try:
        result = eval(expression)
        await message.answer(f"📟 Natija: `{expression} = {result}`", parse_mode="Markdown")
    except ZeroDivisionError:
        await message.answer("❌ Nolga bo'lish mumkin emas!")
    except Exception:
        await message.answer("❌ Misolda xatolik bor.")


@dp.callback_query(F.data == 'language_')
async def show_languages(callback: CallbackQuery, state: FSMContext):
    await state.clear()
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
        ikb.add(InlineKeyboardButton(text=text, callback_data=f'setlang_{code}'))
    ikb.adjust(2)
    await callback.message.answer("Tarjima tilini tanlang:", reply_markup=ikb.as_markup())
    await callback.answer()


@dp.callback_query(F.data.startswith('setlang_'))
async def language_callback(callback: CallbackQuery):
    lang_code = callback.data.split('_')[1]
    user_languages[callback.from_user.id] = lang_code
    await callback.message.answer(f"✅ Til tanlandi. Endi istalgan matningizni yuboring.")
    await callback.answer()


@dp.message(F.text)
async def translate_message(message: Message):
    user_id = message.from_user.id

    if user_id not in user_languages:
        await message.answer("⚠️ Iltimos, avval /start buyrug'i orqali tilni tanlang yoki Kalkulyatorni yoqing!")
        return

    target_lang = user_languages[user_id]
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(message.text)
        await message.answer(f"🌐 **Tarjima ({target_lang}):**\n\n{translated}", parse_mode="Markdown")
    except Exception as e:
        await message.answer("❌ Tarjima qilishda xatolik yuz berdi.")


async def main():
    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi")
