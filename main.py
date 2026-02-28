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


def get_main_menu():
    ikb = InlineKeyboardBuilder()
    ikb.row(
        InlineKeyboardButton(text="Calculator 🔢", callback_data="calcula_"),
        InlineKeyboardButton(text="Languages 🇺🇿", callback_data="language_"),
        InlineKeyboardButton(text="English_dictionary 📚", callback_data="dictionary_")
    )
    ikb.adjust(2)
    return ikb.as_markup()


@dp.message(CommandStart())
async def commands_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="O'zizga kerakli tugmani tanlang!",
        reply_markup=get_main_menu()
    )


@dp.callback_query(F.data == 'dictionary_')
async def show_dictionary(callback: CallbackQuery):
    ikb = InlineKeyboardBuilder()
    ikb.row(
        InlineKeyboardButton(text="Essential Words 1", callback_data="essential_1"),
        InlineKeyboardButton(text="Essential Words 2", callback_data="essential_2"),
        InlineKeyboardButton(text="Essential Words 3", callback_data="essential_3"),
        InlineKeyboardButton(text="Essential Words 4", callback_data="essential_4"),
        InlineKeyboardButton(text="Essential Words 5", callback_data="essential_5"),
        InlineKeyboardButton(text="Destination B1", callback_data="destination_b1"),
        InlineKeyboardButton(text="Destination B1 grammar", callback_data="destination_b1_grammar"),
        InlineKeyboardButton(text="Destination B1\nPhrasal Verbs", callback_data="destinationPhrasal_b1"),
        InlineKeyboardButton(text="Destination B2", callback_data="destination_b2"),
        InlineKeyboardButton(text="Destination B2 grammar", callback_data="destination_b2_grammar"),
        InlineKeyboardButton(text="Destination C1 & C2 grammar", callback_data="destination_c1c2_grammar"),
        InlineKeyboardButton(text="Destination B2,C1-C2\nPhrasal Verbs", callback_data="destinationPhrasal_b2"),
        InlineKeyboardButton(text="Orqaga 🔙", callback_data="back_")
    )
    ikb.adjust(2)
    await callback.message.edit_text("O'zizga kerakli tugmani tanlang!", reply_markup=ikb.as_markup())


@dp.callback_query(F.data == 'essential_1')
async def open_link_essential_1(callback: CallbackQuery):
    pdf_id = "BQACAgIAAxkBAAIB3mmjUlsohT1uttxROP7RhRTOPZfdAAKkCwACDHqJSjV8W4j7y10kOgQ"
    await callback.message.answer_document(document=pdf_id, caption="Mana siz so'ragan Destination 1 kitobi! 📚",
                                           protect_content=True)
    await callback.answer()


@dp.callback_query(F.data == 'essential_2')
async def open_link_essential_2(callback: CallbackQuery):
    pdf_id = "BQACAgIAAxkBAAIB9mmjdR5dxFYYsl71gwj7Aer0YXfcAAKlCwACDHqJSr3ULQxl-Q0jOgQ"
    await callback.message.answer_document(document=pdf_id, caption="Mana siz so'ragan Essential 2 kitobi! 📚",
                                           protect_content=True)
    await callback.answer()


@dp.callback_query(F.data == 'essential_3')
async def open_link_essential_3(callback: CallbackQuery):
    pdf_id = "BQACAgIAAxkBAAIB-GmjdWDKV_i0JNRTfkJIS4UlbAmzAAKmCwACDHqJSg6tquzmMyROOgQ"
    await callback.message.answer_document(document=pdf_id, caption="Mana siz so'ragan Essential 3 kitobi! 📚",
                                           protect_content=True)
    await callback.answer()


@dp.callback_query(F.data == 'essential_4')
async def open_link_essential_4(callback: CallbackQuery):
    pdf_id = "BQACAgIAAxkBAAP7aaNT8whtG7ccvqjOUAw_IWdF3FoAAqcLAAIMeolKyUl9lAUTkaY6BA"
    await callback.message.answer_document(document=pdf_id, caption="Mana siz so'ragan Essential 4 kitobi! 📚",
                                           protect_content=True)
    await callback.answer()


@dp.callback_query(F.data == 'essential_5')
async def open_link_essential_5(callback: CallbackQuery):
    pdf_id = "BQACAgIAAxkBAAP9aaNUL1OSzPLucXxh3twi-6WUA1AAAqgLAAIMeolK2gN_TkCn7-46BA"
    await callback.message.answer_document(document=pdf_id, caption="Mana siz so'ragan Essential 5 kitobi! 📚",
                                           protect_content=True)
    await callback.answer()


@dp.callback_query(F.data == 'destination_b1')
async def open_link_1(callback: CallbackQuery):
    pdf_id = "BQACAgIAAxkBAAPAaaMwr5o5Z_qxXZABMVgRRAtwhr8AArkdAAJUExFIgLaOUQmMjd46BA"
    await callback.message.answer_document(document=pdf_id, caption="Mana siz so'ragan Destination B1 kitobi! 📚",
                                           protect_content=True)
    await callback.answer()


@dp.callback_query(F.data == 'destination_b1_grammar')
async def open_link_1(callback: CallbackQuery):
    pdf_id = "BQACAgIAAxkBAAIBdGmjZwPwFCR7P99nK5EGyNY7H8sbAAKRCgAC_BM4S8SEbYJWsk2IOgQ"
    await callback.message.answer_document(document=pdf_id,
                                           caption="Mana siz so'ragan Destination B1 grammar va lug'at kitobi! 📚",
                                           protect_content=True)
    await callback.answer()


@dp.callback_query(F.data == 'destinationPhrasal_b1')
async def open_link_1(callback: CallbackQuery):
    pdf_id = "BQACAgIAAxkBAAIBfWmjauJ3lU2eZv13csyUI83bB_4GAAJCmQACa6wYSTXAAAEhZo5rOzoE"
    await callback.message.answer_document(document=pdf_id,
                                           caption="Mana siz so'ragan Destination B1 Phrasal Verbs kitobi! 📚",
                                           protect_content=True)
    await callback.answer()


@dp.callback_query(F.data == 'destination_b2')
async def open_link_2(callback: CallbackQuery):
    pdf_id = "BQACAgIAAxkBAAO4aaMvvW3LCrt4GZj86iuBwveaAAHWAAKrGAACVdkxSMSrDLFnpM2tOgQ"

    await callback.message.answer_document(document=pdf_id, caption="Mana siz so'ragan Destination B2 kitobi! 📚",
                                           protect_content=True)
    await callback.answer()


@dp.callback_query(F.data == 'destination_b2_grammar')
async def open_link_2(callback: CallbackQuery):
    pdf_id = "BQACAgIAAxkBAAIBeWmjaDfxzN6jTSemTRvSMOWJu4NRAAKpHQACVBMRSCnJM6qmgBugOgQ"

    await callback.message.answer_document(document=pdf_id,
                                           caption="Mana siz so'ragan Destination B2 grammar kitobi! 📚",
                                           protect_content=True)
    await callback.answer()


@dp.callback_query(F.data == 'destinationPhrasal_b2')
async def open_link_3(callback: CallbackQuery):
    pdf_id = "BQACAgIAAxkBAAPjaaM5qDy57Vv_bfJVYXmHlXxoViMAAqYdAAJUExFIfKKLtdyo5_k6BA"

    await callback.message.answer_document(document=pdf_id,
                                           caption="Mana siz so'ragan Destination B2,C1,C2 Prasal Verbs So'zlari! 📚",
                                           protect_content=True)
    await callback.answer()


@dp.callback_query(F.data == 'destination_c1c2_grammar')
async def open_link_3(callback: CallbackQuery):
    pdf_id = "BQACAgIAAxkBAAIBe2mjaWhgvupaz6w1DbsPgf2PL7WxAALdHQACVBMRSLhTM4sN3yEFOgQ"

    await callback.message.answer_document(document=pdf_id,
                                           caption="Mana siz so'ragan Destination C1,C2 grammar kitobi! 📚",
                                           protect_content=True)
    await callback.answer()


@dp.callback_query(F.data == "back_")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(text="O'zizga kerakli tugmani tanlang!", reply_markup=get_main_menu())

    await callback.answer()


@dp.message(F.document)
async def get_file_id_handler(message: Message):
    file_id = message.document.file_id
    await message.reply(f"Fayl ID nusxalab oling:\n\n<code>{file_id}</code>", parse_mode="HTML")
    print(f"TERMINALDA HAM CHIQADI: {file_id}")


@dp.callback_query(F.data == 'calcula_')
async def start_calc(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BotState.waiting_for_example)
    await callback.message.answer("📊 Kalkulyator rejimi yoqildi.\n\nMisolni yozing (masalan: 80+10*(55/11)):")
    await callback.answer()


@dp.message(BotState.waiting_for_example)
async def calculate_math(message: Message, state: FSMContext):
    await state.clear()
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
    await callback.message.delete()
    await state.clear()
    ikb = InlineKeyboardBuilder()
    languages = [
        ('O‘zbek 🇺🇿', 'uz'), ('Rus 🇷🇺', 'ru'), ('Ingliz 🇬🇧', 'en'), ('Arab 🇸🇦', 'ar'),
    ]
    for text, code in languages:
        ikb.add(InlineKeyboardButton(text=text, callback_data=f'setlang_{code}'))
    ikb.adjust(2)
    ikb.row(InlineKeyboardButton(text='Back 🔙', callback_data='back_'))
    await callback.message.answer("Tarjima tilini tanlang:", reply_markup=ikb.as_markup())
    await callback.answer()


@dp.callback_query(F.data.startswith('setlang_'))
async def language_callback(callback: CallbackQuery):
    lang_code = callback.data.split('_')[1]
    user_languages[callback.from_user.id] = lang_code
    await callback.message.answer(f"✅ Til tanlandi. Endi istalgan matningizni yuboring.")

    await callback.answer()


@dp.callback_query(F.data == 'back_')
async def go_back_to_main(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()

    await callback.message.answer(text="Asosiy menyuga qaytingiz. O'zizga kerakli tugmani bosing:",
                                  reply_markup=get_main_menu())
    await callback.answer()


@dp.message(F.text)
async def translate_message(message: Message):
    user_id = message.from_user.id

    if user_id not in user_languages:
        await message.answer(
            "⚠️ Iltimos, avval /start buyrug'i orqali o'zizga kerakli tugmani tanlang keyin qayta ishlating!")
        return

    target_lang = user_languages[user_id]
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(message.text)
        await message.answer(f"🌐 **Tarjima ({target_lang}):**\n\n{translated}", parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"❌ Tarjima qilishda xatolik yuz berdi., {e}")


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
