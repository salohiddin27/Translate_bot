import asyncio
import logging
import os
import random

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, BotCommand, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
from gtts import gTTS

from mixed_present import MIXED_PRESENT_QUIZ
from present_continuous import PRESENT_CONTINUOUS_QUIZ
from present_perfect import PRESENT_PERFECT_QUIZ
from present_simple import PRESENT_SIMPLE_QUIZ

logging.basicConfig(level=logging.INFO)

load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

quiz_data = {}
user_languages = {}


class BotState(StatesGroup):
    waiting_for_example = State()


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='start', description='Botni ishga tushirish 🔄'),
        BotCommand(command='stop', description="Testni to'xtatish ❌"),
    ]
    await bot.set_my_commands(main_menu_commands)


def get_main_menu():
    ikb = InlineKeyboardBuilder()
    ikb.row(
        InlineKeyboardButton(text="Calculator 🔢", callback_data="calcula_"),
        InlineKeyboardButton(text="Languages 🇺🇿", callback_data="language_"),
        InlineKeyboardButton(text="English dictionary 📚", callback_data="dictionary_"),
        InlineKeyboardButton(text="Games 🚗", callback_data="game_"),
        InlineKeyboardButton(text="English Tests 📝", callback_data="english_test"),
    )
    ikb.adjust(2)
    return ikb.as_markup()


@dp.message(CommandStart())
async def commands_start(message: types.Message, state: FSMContext):
    await state.clear()

    text = "Please choose the button you need?"
    audio_path = "audios/welcome.mp3"

    tts = gTTS(text=text, lang="en", tld="co.uk")
    tts.save(audio_path)

    await message.answer_voice(
        voice=FSInputFile(audio_path),
        caption=text,
        reply_markup=get_main_menu()
    )


@dp.callback_query(F.data == 'english_test')
async def english_test(callback: CallbackQuery):
    await callback.message.delete()
    ikb = InlineKeyboardBuilder()
    ikb.row(
        InlineKeyboardButton(text="Present Simple", callback_data="quiz_ps"),
        InlineKeyboardButton(text="Present Continuous", callback_data="quiz_pc"),
        InlineKeyboardButton(text="Present Perfect", callback_data="quiz_pp"),
        InlineKeyboardButton(text="Mixed Present ", callback_data="quiz_mp"),
        InlineKeyboardButton(text="Back ←", callback_data="back_")
    )
    ikb.adjust(2)
    await callback.message.answer("Qaysi zamon bo'yicha test topshirmoqchisiz?", reply_markup=ikb.as_markup())


@dp.callback_query(F.data.startswith('quiz_'))
async def start_universal_quiz(callback: CallbackQuery):
    await callback.message.delete()
    user_id = callback.from_user.id

    quiz_type = callback.data.replace('quiz_', '')

    if quiz_type == 'ps':
        questions_pool = PRESENT_SIMPLE_QUIZ
        title = "Present Simple"
    elif quiz_type == 'pc':
        questions_pool = PRESENT_CONTINUOUS_QUIZ
        title = "Present Continuous"
    elif quiz_type == 'pp':
        questions_pool = PRESENT_PERFECT_QUIZ
        title = "Present Perfect"
    elif quiz_type == 'mp':
        questions_pool = MIXED_PRESENT_QUIZ
        title = "Mixed Present"
    else:
        return

    quiz_data[user_id] = {"score": 0, "correct_options": {}, "is_active": True}

    k_count = min(len(questions_pool), 30)
    selected_questions = random.sample(questions_pool, k=k_count)

    await callback.message.answer(f"🚀 {title} testi boshlandi! Jami savollar: {k_count} ta.")

    for item in selected_questions:
        if user_id not in quiz_data or not quiz_data[user_id].get("is_active"):
            return

        msg = await callback.message.answer_poll(
            question=item['q'],
            options=item['o'],
            correct_option_id=item['c'],
            type='quiz',
            open_period=15,
            is_anonymous=False
        )

        quiz_data[user_id]["correct_options"][msg.poll.id] = item['c']
        await asyncio.sleep(15)

    if user_id in quiz_data and quiz_data[user_id].get("is_active"):
        final_score = quiz_data[user_id]["score"]
        await callback.message.answer(
            f"✅ Test tugadi!\nNatijangiz: {k_count} tadan {final_score} ta to'g'ri topdingiz."
        )
        del quiz_data[user_id]
        await callback.message.answer("Asosiy menyuga qaytdingiz:", reply_markup=get_main_menu())


@dp.poll_answer()
async def handle_poll_answer(poll_answer: types.PollAnswer):
    user_id = poll_answer.user.id
    poll_id = poll_answer.poll_id

    if user_id in quiz_data:
        correct_id = quiz_data[user_id]["correct_options"].get(poll_id)
        if poll_answer.option_ids[0] == correct_id:
            quiz_data[user_id]["score"] += 1


@dp.message(Command("stop"))
async def process_stop_command(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in quiz_data:
        quiz_data[user_id]["is_active"] = False

    await state.clear()
    await message.answer("Asosiy menyu:", reply_markup=get_main_menu())


@dp.callback_query(F.data == 'back_')
async def get_to_main(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    await callback.message.answer(text="Asosiy menyu:", reply_markup=get_main_menu())


@dp.callback_query(F.data == 'game_')
async def show_all_cars(callback: CallbackQuery):
    await callback.message.delete()
    ikb = InlineKeyboardBuilder()
    ikb.row(
        InlineKeyboardButton(text="Lightweight car 🚘", callback_data="ligt_cars"),
        InlineKeyboardButton(text="Truck 🚛", callback_data="track_"),
        InlineKeyboardButton(text="Motorbikes 🏍️", callback_data="motor_bice_"),
        InlineKeyboardButton(text="Archery game 🏹", callback_data="kamon_"),
        InlineKeyboardButton(text="Back ←", callback_data="back_"),
    )
    ikb.adjust(2)
    await callback.message.answer("O'zizga yoqgan o'yini tanlang! ", reply_markup=ikb.as_markup())


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
            InlineKeyboardButton(text="Back ←", callback_data="back_"),

            )
    ikb.adjust(2)
    await callback.message.answer(f"O'zizga yoqgan o'yini tanlang! ", reply_markup=ikb.as_markup())


@dp.callback_query(F.data == 'war_')
async def show_war(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.maxgames.stickwarlegacy"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'archers_')
async def show_archers(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.byv.TheArchers2"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'ninja_')
async def show_ninja(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=ninja.creed.sniper.real3d.action.free.android"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'birds_')
async def show_birds(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.rovio.angrybirdsfriends"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'immortal_')
async def show_immortal(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.wolffun.thetanimmortal"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'shooter_')
async def show_shooter(callback: CallbackQuery):
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
            InlineKeyboardButton(text="Back ←", callback_data="back_"),

            )
    ikb.adjust(2)
    await callback.message.answer("Yoqgan O'yini tanlang! ", reply_markup=ikb.as_markup())


@dp.callback_query(F.data == 'motor_bike_')
async def show_bike(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.skgames.trafficrider"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'bike_stunt_')
async def show_stunt(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.gt.moto.bike.wheelie.stunt.race.game"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'bike_')
async def show_bikes(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.kn.bikestunt3.racing.driving.games"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'race_')
async def show_race(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.offline.racing.motorcyclegame.motomax.bikerace.bike.games"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'mountain_bike_')
async def show_mountain_bike(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.PixelJoy.MountainBikeXtreme"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'blast_')
async def show_blast(callback: CallbackQuery):
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
            InlineKeyboardButton(text="Offoard Truck 🚚", callback_data="offard_"),
            InlineKeyboardButton(text="Truck Star 🚛", callback_data="star_"),
            InlineKeyboardButton(text="Back ←", callback_data="back_")

            )
    ikb.adjust(2)
    await callback.message.answer("O'zizga yoqgan o'yini tanlang! ", reply_markup=ikb.as_markup())


@dp.callback_query(F.data == 'simulator_t')
async def get_truc(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.zuuks.truck.simulator.ultimate"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'europa_')
async def get_europa(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.WandaSoftware.TruckersofEurope3"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'school_')
async def get_school(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.bettergames.truck.drivingschool.simulator"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'ww2_')
async def get_ww2(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=truck.simulator.climb.frontline"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'offard_')
async def get_offard(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.pw.trucksimulatoreuro.offroadcargo"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'star_')
async def get_star(callback: CallbackQuery):
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
        InlineKeyboardButton(text="Need for Speed 🏎️", callback_data="speed_"),
        InlineKeyboardButton(text="MIMX Hill Dash 🛻", callback_data="dash_"),
        InlineKeyboardButton(text="Car Crash Royale ⛔", callback_data="crash_"),
        InlineKeyboardButton(text="Back ←", callback_data="back_"),

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
async def show_driving(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.ansangha.drdriving"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'racer_')
async def show_racer(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.skgames.trafficracer"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'mountain_climb_')
async def show_mountainclimb(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.dagtirmanma.oyunu"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'stock_car_')
async def show_stock_car(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.minicades.stockcars"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'extreme_')
async def show_extreme(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.aim.racing"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'speed_')
async def show_speed(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.ea.game.nfs14_row"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'dash_')
async def show_dash(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.hutchgames.hilldash2"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == 'crash_')
async def show_crash(callback: CallbackQuery):
    url = "https://play.google.com/store/apps/details?id=com.FailGames.RoyalCarDestroy"
    await callback.message.answer(f"Siz so'ragan mashina umid qilamanki bu o'yin sizga yoqadi 😊\n\n{url}")


@dp.callback_query(F.data == "back_")
async def get_to_main(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()

    await callback.message.answer(text="Asosiy menyuga qaytingiz. O'zizga kerakli tugmani bosing:",
                                  reply_markup=get_main_menu())
    await callback.answer()


books_list = [
    ("Essential Words 1", "essential_1"),
    ("Essential Words 2", "essential_2"),
    ("Essential Words 3", "essential_3"),
    ("Essential Words 4", "essential_4"),
    ("Essential Words 5", "essential_5"),
    ("Destination B1", "destination_b1"),
    ("Destination B1 grammar", "destination_b1_grammar"),
    ("Destination B1Phrasal Verbs", "destinationPhrasal_b1"),
    ("Destination B2", "destination_b2"),
    ("Destination B2 grammar", "destination_b2_grammar"),
    ("Destination C1 & C2 grammar", "destination_c1c2_grammar"),
    ("Destination B2,C1-C2 Phrasal Verbs", "destinationPhrasal_b2"),
    ("Cambridge Vocabulary for IElTS", "cambridge_")
]


@dp.callback_query(F.data == 'dictionary_')
async def show_dictionary(callback: CallbackQuery):
    ikb = InlineKeyboardBuilder()

    for title, call_data in books_list[0:6]:
        ikb.row(InlineKeyboardButton(text=title, callback_data=call_data))

    ikb.row(
        InlineKeyboardButton(text="← Back", callback_data="back_"),  # Asosiy menyuga
        InlineKeyboardButton(text="Next →", callback_data="next:6")  # 2-sahifaga
    )

    ikb.adjust(1)
    await callback.message.edit_text("Lug'at bo'limi. 1-sahifa", reply_markup=ikb.as_markup())
    await callback.answer()


@dp.callback_query(F.data.startswith("next:"))
async def after_next(callback: CallbackQuery):
    current_index = int(callback.data.split(":")[1])

    if current_index == 0:
        await show_dictionary(callback)
        return

    current_books = books_list[current_index: current_index + 6]

    if not current_books:
        await callback.answer("Boshqa kitob qolmadi!", show_alert=True)
        return

    ikb = InlineKeyboardBuilder()

    for title, call_data in current_books:
        ikb.row(InlineKeyboardButton(text=title, callback_data=call_data))

    nav_buttons = []

    back_target = f"next:{current_index - 6}"
    nav_buttons.append(InlineKeyboardButton(text="← Back", callback_data=back_target))

    if current_index + 6 < len(books_list):
        nav_buttons.append(InlineKeyboardButton(text="Next →", callback_data=f"next:{current_index + 6}"))

    ikb.row(*nav_buttons)
    ikb.adjust(1)

    page_num = current_index // 6 + 1
    await callback.message.edit_text(
        f"Lug'at bo'limi. {page_num}-sahifa",
        reply_markup=ikb.as_markup()
    )
    await callback.answer()


@dp.callback_query(F.data == "back_")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        text="O'zizga kerakli tugmani tanlang!",
        reply_markup=get_main_menu()
    )
    await callback.answer()


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


@dp.callback_query(F.data == 'cambridge_')
async def cambridge_link(callback: CallbackQuery):
    pdf_id = "BQACAgQAAxkBAAIDommm0ZYE4DBt8Ns8Diaup5bnufdQAAKeDAACAm-YU9CZPa3vuGJDOgQ"

    await callback.message.answer_document(document=pdf_id,
                                           caption="Mana siz so'ragan 'Cambridge Vocabulary for IELTS' kitobi! 📚",
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
    ikb.row(InlineKeyboardButton(text='Back ←', callback_data='back_'))
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
