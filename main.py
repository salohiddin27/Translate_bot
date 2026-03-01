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
        InlineKeyboardButton(text="English_dictionary 📚", callback_data="dictionary_"),
        InlineKeyboardButton(text="Games 🚗", callback_data="game_")
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


@dp.callback_query(F.data == 'game_')
async def show_all_cars(callback: CallbackQuery):
    await callback.message.delete()
    ikb = InlineKeyboardBuilder()
    ikb.row(
        InlineKeyboardButton(text="Lightweight car 🚘", callback_data="ligt_cars"),
        InlineKeyboardButton(text="Truck 🚛", callback_data="track_"),
        InlineKeyboardButton(text="Motorbikes 🏍️", callback_data="motor_bice_"),
        InlineKeyboardButton(text="Archery game 🏹", callback_data="kamon_"),
        InlineKeyboardButton(text="Back 🔙", callback_data="back_"),
    )
    ikb.adjust(2)
    await callback.message.answer(f"O'zizga yoqgan o'yini tanlang! ", reply_markup=ikb.as_markup())


@dp.callback_query(F.data == 'back_')
async def get_to_main(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    await callback.message.answer(text="Asosiy menyuga qaytingiz. O'zizga kerakli tugmani bosing:",
                                  reply_markup=get_main_menu())


@dp.callback_query(F.data == 'kamon_')
async def show_shot(callback: CallbackQuery):
    await callback.message.delete()
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text="Stik War ⚔️", callback_data="war_"),
            InlineKeyboardButton(text="The Archers 2 🏹", callback_data="archers_"),
            InlineKeyboardButton(text="Ninja's Creed: 3D 🥷", callback_data="ninja_"),
            InlineKeyboardButton(text="Angry Birds 🐦", callback_data="birds_"),
            InlineKeyboardButton(text="Thetan Immortal 🦸", callback_data="immortal_"),
            InlineKeyboardButton(text="Archer Shooter 🏹🎯", callback_data="shooter_"),
            InlineKeyboardButton(text="Back 🔙", callback_data="back_"),

            )
    ikb.adjust(2)
    await callback.message.answer(f"O'zizga yoqgan o'yini tanlang! ", reply_markup=ikb.as_markup())


@dp.callback_query(F.data == 'war_')
async def show_war(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.maxgames.stickwarlegacy"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'archers_')
async def show_war(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.byv.TheArchers2"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'ninja_')
async def show_war(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=ninja.creed.sniper.real3d.action.free.android"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'birds_')
async def show_war(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.rovio.angrybirdsfriends"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'immortal_')
async def show_war(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.wolffun.thetanimmortal"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'shooter_')
async def show_war(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.action_games.archer.shooter.attack"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'back_')
async def get_to_main(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    await callback.message.answer(text="Asosiy menyuga qaytingiz. O'zizga kerakli tugmani bosing:",
                                  reply_markup=get_main_menu())


@dp.callback_query(F.data == 'motor_bice_')
async def show_motor_bice(callback: CallbackQuery):
    await callback.message.delete()
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text="Traffic Rider 🏍️", callback_data="motor_bike_"),
            InlineKeyboardButton(text="Moto Bike Stunt 🏍️💨", callback_data="bike_stunt_"),
            InlineKeyboardButton(text="Bike Racing 3D 🚴🏻‍♂️", callback_data="bike_"),
            InlineKeyboardButton(text="MRM Bike Racing 🏍️🏁", callback_data="race_"),
            InlineKeyboardButton(text="Mountain Bike 🚵", callback_data="mountain_bike_"),
            InlineKeyboardButton(text="Bike Blast 🚴🏻‍♂️", callback_data="blast_"),
            InlineKeyboardButton(text="Back 🔙", callback_data="back_"),

            )
    ikb.adjust(2)
    await callback.message.answer("Yoqgan O'yini tanlang! ", reply_markup=ikb.as_markup())


@dp.callback_query(F.data == 'motor_bike_')
async def show_moto(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.skgames.trafficrider"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'bike_stunt_')
async def show_moto(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.gt.moto.bike.wheelie.stunt.race.game"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'bike_')
async def show_moto(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.kn.bikestunt3.racing.driving.games"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'race_')
async def show_moto(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.offline.racing.motorcyclegame.motomax.bikerace.bike.games"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'mountain_bike_')
async def show_moto(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.PixelJoy.MountainBikeXtreme"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'blast_')
async def show_moto(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.aceviral.bmxblast"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'back_')
async def get_to_main(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    await callback.message.answer(text="Asosiy menyuga qaytingiz. O'zizga kerakli tugmani bosing:",
                                  reply_markup=get_main_menu())


@dp.callback_query(F.data == 'track_')
async def show_truck(callback: CallbackQuery):
    await callback.message.delete()
    ikb = InlineKeyboardBuilder()
    ikb.row(InlineKeyboardButton(text="Truck Simulator 🚛", callback_data="simulator_t"),
            InlineKeyboardButton(text="Truckers of Europe 3 🚚", callback_data="europa_"),
            InlineKeyboardButton(text="Truck Driving School 🚚", callback_data="school_"),
            InlineKeyboardButton(text="Frontline WW2 ⛓️", callback_data="ww2_"),
            InlineKeyboardButton(text="Offoard Truck 🚚", callback_data="offfard_"),
            InlineKeyboardButton(text="Truck Star 🚛", callback_data="star_"),
            InlineKeyboardButton(text="Back 🔙", callback_data="back_")

            )
    ikb.adjust(2)
    await callback.message.answer("O'zizga yoqgan o'yini tanlang! ", reply_markup=ikb.as_markup())


@dp.callback_query(F.data == 'simulator_t')
async def get_truc(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.zuuks.truck.simulator.ultimate"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'europa_')
async def get_truc(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.WandaSoftware.TruckersofEurope3"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'school_')
async def get_truc(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.bettergames.truck.drivingschool.simulator"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'ww2_')
async def get_truc(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=truck.simulator.climb.frontline"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'offfard_')
async def get_truc(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.pw.trucksimulatoreuro.offroadcargo"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'star_')
async def get_truc(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.vm3.global"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'back_')
async def get_to_main(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    await callback.message.answer(text="Asosiy menyuga qaytingiz. O'zizga kerakli tugmani bosing:",
                                  reply_markup=get_main_menu())
    await callback.answer()


@dp.callback_query(F.data == 'ligt_cars')
async def show_car(callback: CallbackQuery):
    ikb = InlineKeyboardBuilder()
    ikb.row(
        InlineKeyboardButton(text="Payback 2 🚘", callback_data="payback_"),
        InlineKeyboardButton(text="Hill Climb racing 🛻", callback_data="hill_climb_"),
        InlineKeyboardButton(text="Dr.Driving 🚘", callback_data="driving_"),
        InlineKeyboardButton(text="Traffic Racer 🏎️", callback_data="racer_"),
        InlineKeyboardButton(text="Mountain Climb 🚘", callback_data="mountain_climb_"),
        InlineKeyboardButton(text="Stock Car Racing 🏎️", callback_data="stock_car_"),
        InlineKeyboardButton(text="Extreme Car 🏎", callback_data="extreme_"),
        InlineKeyboardButton(text="Traffic racer 🏎️", callback_data="racer_"),
        InlineKeyboardButton(text="MIMX Hill Dash 🛻", callback_data="dash_"),
        InlineKeyboardButton(text="Car Crash Royale ⛔", callback_data="crash_"),
        InlineKeyboardButton(text="Back 🔙", callback_data="back_"),

    )
    ikb.adjust(2)
    await callback.message.edit_text("O'zizga yoqgan o'yini tanlang!", reply_markup=ikb.as_markup())


@dp.callback_query(F.data == "payback_")
async def show_payback(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=net.apex_designs.payback2"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'hill_climb_')
async def show_hill_climb(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.fingersoft.hillclimb"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'driving_')
async def show_hill_climb(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.ansangha.drdriving"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'racer_')
async def show_hill_climb(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.skgames.trafficracer"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'mountain_climb_')
async def show_hill_climb(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.dagtirmanma.oyunu"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'stock_car_')
async def show_hill_climb(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.minicades.stockcars"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'extreme_')
async def show_hill_climb(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.aim.racing"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'racer_')
async def show_hill_climb(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.skgames.trafficracer"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'dash_')
async def show_hill_climb(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.hutchgames.hilldash2"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'crash_')
async def show_hill_climb(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.FailGames.RoyalCarDestroy"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == "back_")
async def get_to_main(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()

    await callback.message.answer(text="Asosiy menyuga qaytingiz. O'zizga kerakli tugmani bosing:",
                                  reply_markup=get_main_menu())
    await callback.answer()


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
    pdf_id = "BQACAgIAAxkBAAIB_mmjdc4EjQQD5fWh0tJkJMsRnMY4AAKnCwACDHqJSvn-JZHdvP4qOgQ"
    await callback.message.answer_document(document=pdf_id, caption="Mana siz so'ragan Essential 4 kitobi! 📚",
                                           protect_content=True)
    await callback.answer()


@dp.callback_query(F.data == 'essential_5')
async def open_link_essential_5(callback: CallbackQuery):
    pdf_id = "BQACAgIAAxkBAAICAAFpo3XxfsnqoHn9iYOzyogR5t4FdwACqAsAAgx6iUqGDZZcu61DAjoE"
    await callback.message.answer_document(document=pdf_id, caption="Mana siz so'ragan Essential 5 kitobi! 📚",
                                           protect_content=True)
    await callback.answer()


@dp.callback_query(F.data == 'destination_b1')
async def open_link_1(callback: CallbackQuery):
    pdf_id = "BQACAgIAAxkBAAICAmmjdh1TihU6Pm52oDdSbZpwpyoyAAK5HQACVBMRSF7seBxIPuTbOgQ"
    await callback.message.answer_document(document=pdf_id, caption="Mana siz so'ragan Destination B1 kitobi! 📚",
                                           protect_content=True)
    await callback.answer()


@dp.callback_query(F.data == 'destination_b1_grammar')
async def open_link_1(callback: CallbackQuery):
    pdf_id = "BQACAgIAAxkBAAICBGmjdk5BTbuatOHy6Ej9oI5hn0UPAAKoAgACJgnoSqoGoJrb0slDOgQ"
    await callback.message.answer_document(document=pdf_id,
                                           caption="Mana siz so'ragan Destination B1 grammar va lug'at kitobi! 📚",
                                           protect_content=True)
    await callback.answer()


@dp.callback_query(F.data == 'destinationPhrasal_b1')
async def open_link_1(callback: CallbackQuery):
    pdf_id = "BQACAgIAAxkBAAICBmmjdnahiWKonKN-BfK5w_h7iBZWAAK2iQACBMohSUn-e2FHQaNoOgQ"
    await callback.message.answer_document(document=pdf_id,
                                           caption="Mana siz so'ragan Destination B1 Phrasal Verbs kitobi! 📚",
                                           protect_content=True)
    await callback.answer()


@dp.callback_query(F.data == 'destination_b2')
async def open_link_2(callback: CallbackQuery):
    pdf_id = "BQACAgIAAxkBAAICCGmjdp671sjJzkTG_562dX1Ey519AAKrGAACVdkxSGyxufhxFFwfOgQ"

    await callback.message.answer_document(document=pdf_id, caption="Mana siz so'ragan Destination B2 kitobi! 📚",
                                           protect_content=True)
    await callback.answer()


@dp.callback_query(F.data == 'destination_b2_grammar')
async def open_link_2(callback: CallbackQuery):
    pdf_id = "BQACAgIAAxkBAAICCmmjds7VjnVuBwMdJVdNMqjhTxpHAAKpHQACVBMRSE-H52CYv6OoOgQ"

    await callback.message.answer_document(document=pdf_id,
                                           caption="Mana siz so'ragan Destination B2 grammar kitobi! 📚",
                                           protect_content=True)
    await callback.answer()


@dp.callback_query(F.data == 'destinationPhrasal_b2')
async def open_link_3(callback: CallbackQuery):
    pdf_id = "BQACAgIAAxkBAAICDGmjdvE90-5Mz2OcDr6rpTJibPMmAAKmHQACVBMRSDsVublbMSskOgQ"

    await callback.message.answer_document(document=pdf_id,
                                           caption="Mana siz so'ragan Destination B2,C1,C2 Prasal Verbs So'zlari! 📚",
                                           protect_content=True)
    await callback.answer()


@dp.callback_query(F.data == 'destination_c1c2_grammar')
async def open_link_3(callback: CallbackQuery):
    pdf_id = "BQACAgIAAxkBAAICDmmjdy8ZM6-Fc-BHmV06jF0i0uXSAALdHQACVBMRSMlTchFYGUafOgQ"

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
