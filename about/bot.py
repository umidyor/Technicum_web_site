import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # ✅ Import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
import requests,json
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType
from functools import wraps
superadmin=5149506457






from env import BOT_TOKEN,ADMINS
YOUR_WEBSITE_URL = "https://parkentpolitexnikum.uz/"
logging.basicConfig(level=logging.INFO)

# ✅ Fix: Add MemoryStorage to Dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
CHANNELS = {
    'parkenttumaanpolitexnikumi': "ParkenPolitexnikumRasmiyðŸ“Œ",
}

import pandas as pd

def csv_to_excel(input_csv, output_excel):
    df = pd.read_csv(input_csv)
    df.to_excel(output_excel, index=False)
    print(f"{input_csv} muvaffaqiyatli {output_excel} ga o'tkazildi!")




from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, ln=True, align='C')

    def get_num_lines(self, text, col_width):
        """Matnni nechta qatorga bo'lishini hisoblash"""
        self.set_font("Arial", size=9)
        return len(self.multi_cell(col_width, 6, text, border=0, align='L', split_only=True))


def csv_to_pdf(input_csv, output_pdf):
    df = pd.read_csv(input_csv)

    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=9)

    # **Aniq ustun kengliklari (jami 9 ta ustun sig‘ishi uchun)**
    col_widths = [20, 25, 30, 20, 40, 30, 35, 45, 30]  # Har bir ustun kengligi

    # **Jadval sarlavhalari**
    for i, col in enumerate(df.columns):
        pdf.cell(col_widths[i], 8, col, border=1, align='C')
    pdf.ln()

    # **CSV ma'lumotlarini PDF ga yozish**
    for _, row in df.iterrows():
        row_data = [str(cell) for cell in row]

        # **Matnning nechta qatorga bo‘linishini hisoblash**
        max_lines = max(pdf.get_num_lines(cell, col_widths[i]) for i, cell in enumerate(row_data))

        # **Multi-line qator yozish**
        for line in range(max_lines):
            for i, cell in enumerate(row_data):
                cell_lines = pdf.multi_cell(col_widths[i], 6, cell, border=0, align='L', split_only=True)
                text = cell_lines[line] if line < len(cell_lines) else ""
                pdf.cell(col_widths[i], 6, text, border=1, align='L')
            pdf.ln()

    # **PDF faylni saqlash**
    pdf.output(output_pdf)
    print(f"{input_csv} muvaffaqiyatli {output_pdf} ga o'tkazildi!")


async def is_subscribed(user_id: int) -> bool:
    try:
        for usename,name in CHANNELS.items():
            member = await bot.get_chat_member(f"@{usename}", user_id)
            return member.status in ['member', 'administrator', 'creator']
    except Exception:
        return False
async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Botni ishga tushirish"),
        types.BotCommand("stop", "Ro'yxatdan o'tishni to'xtatish")
    ])

# def check_subscription():
#     """Decorator: Foydalanuvchini kanalda bor yoki yo‘qligini tekshiradi"""
#
#     def decorator(func):
#         @wraps(func)
#         async def wrapper(message: types.Message, *args, **kwargs):
#             not_subscribed_channels = [
#                 name for name, username in CHANNELS.items()
#                 if not await is_subscribed(message.from_user.id, username)
#             ]
#
#             if not_subscribed_channels:
#                 keyboard = InlineKeyboardMarkup(row_width=1)
#                 for name, username in CHANNELS.items():
#                     keyboard.add(InlineKeyboardButton(f"✅ {username}", url=f"https://t.me/{name}"))
#
#                 keyboard.add(InlineKeyboardButton("🔄 Tekshirish", callback_data="check_sub"))
#
#                 await message.answer(
#                     "❌ Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:",
#                     reply_markup=keyboard
#                 )
#                 return
#
#             return await func(message, *args, **kwargs)
#
#         return wrapper
#
#     return decorator


# Start handler


# Callback handler - "Tekshirish" tugmasi



def get_majors():
    url = "https://parkentpolitexnikum.uz/api/courses"
    API_KEY = "hCw6Cj6G.K7bmo7C4JWufviGW0VpDKUZPrBjttLSy"

    headers = {"Authorization": f"Api-Key {API_KEY}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return [course["course_name"] for course in data]
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []  # ✅ Prevents `NoneType` errors


async def set_web_app_button():
    menu_button = types.MenuButtonWebApp(
        text="Rasmiy sayt📴",
        web_app=types.WebAppInfo(url=YOUR_WEBSITE_URL)
    )
    await bot.set_chat_menu_button(menu_button=menu_button)

class RegisterStates(StatesGroup):
    major = State()
    full_name = State()
    age = State()
    location = State()
    phone = State()
    student_class = State()
    system = State()
    confirm = State()
    result=State()

class SuggestState(StatesGroup):
    suggest=State()



import csv
def get_user_ids():

    try:
        user_ids = []
        with open("registered_users.csv", mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if row:
                    try:
                        user_ids.append(int(row[0]))
                    except ValueError:
                        pass
        return user_ids
    except:
        print("Fayl topilmadi")

class AdminSet(StatesGroup):
    admin_id=State()

@dp.message_handler(commands=['admin'])
async def set_admin(message:types.Message):
    if message.from_user.id==superadmin:
        await message.reply("Assalom alekum MR Cristiano🐐, bugun kimni admin qilmoqchisiz?")
        await AdminSet.admin_id.set()

    else:
        with open("sticker.webp", "rb") as sticker:
            await bot.send_sticker(chat_id=message.chat.id, sticker=sticker)




@dp.message_handler(state=AdminSet.admin_id)
async def save_admin(message: types.Message,state: FSMContext):
    global ADMINS
    admin_id=message.text
    with open("Admins.txt", "a", encoding="utf-8") as f:
        f.write(admin_id + "\n")
    await message.reply("Ushbu admin saqlandi🙏")

    await state.finish()
    ADMINS.append(int(message.text))

class Chat(StatesGroup):
    chat_id=State()
    chat=State()


@dp.message_handler(commands=['chat'])
async def chat_to(message: types.Message):
    if message.from_user.id == superadmin:
        await message.reply("Assalom alekum MR Cristiano🐐, Xabar kim uchun(id)??")
        await Chat.chat_id.set()
    else:
        with open("sticker.webp", "rb") as sticker:
            await bot.send_sticker(chat_id=message.chat.id, sticker=sticker)


@dp.message_handler(state=Chat.chat_id)
async def save_admin(message: types.Message, state: FSMContext):
    chat_id = message.text
    await state.update_data(chat_id=chat_id)
    await message.reply("Endi esa nima yozmoqchisiz? (Matn, rasm, gif, video, sticker, yoki fayl yuboring)")
    await Chat.next()


@dp.message_handler(state=Chat.chat, content_types=[
    ContentType.TEXT, ContentType.PHOTO, ContentType.VIDEO, ContentType.ANIMATION,
    ContentType.DOCUMENT, ContentType.STICKER, ContentType.VOICE, ContentType.AUDIO
])
async def send_message_to_chat(message: types.Message, state: FSMContext):
    data = await state.get_data()
    chat_id = data['chat_id']

    try:
        # TEXT messages
        if message.text:
            await bot.send_message(chat_id=chat_id, text=message.text)

        # PHOTO
        elif message.photo:
            await bot.send_photo(chat_id=chat_id, photo=message.photo[-1].file_id, caption=message.caption)

        # VIDEO
        elif message.video:
            await bot.send_video(chat_id=chat_id, video=message.video.file_id, caption=message.caption)

        # GIF (Animation)
        elif message.animation:
            await bot.send_animation(chat_id=chat_id, animation=message.animation.file_id, caption=message.caption)

        # DOCUMENT (PDF, TXT, etc.)
        elif message.document:
            await bot.send_document(chat_id=chat_id, document=message.document.file_id, caption=message.caption)

        # STICKER
        elif message.sticker:
            await bot.send_sticker(chat_id=chat_id, sticker=message.sticker.file_id)

        # VOICE MESSAGE
        elif message.voice:
            await bot.send_voice(chat_id=chat_id, voice=message.voice.file_id)

        # AUDIO (MP3, etc.)
        elif message.audio:
            await bot.send_audio(chat_id=chat_id, audio=message.audio.file_id, caption=message.caption)

        await state.finish()

    except Exception as e:
        await message.reply(f"Xatolik yuz berdi:\n{str(e)}")
        await state.finish()

new_users=set()
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):

    user_ids_list = get_user_ids()
    chat_member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)

    if message.from_user.id not in new_users:
        new_users.add(message.from_user.id)
        await bot.send_message(chat_id=superadmin,text="👋Botga yangi qo‘shilgan user"
                f"<a href='tg://user?id={message.from_user.id}'>Telegram id: [{message.from_user.id}]</a>"
                f"\n<a href='https://t.me/{message.from_user.username}'>Telegram username: [{message.from_user.username}]</a>"
                f"\n<a href='https://t.me/{message.from_user.username}'>Telegram username: [{message.from_user.full_name}]</a>\n",
                               parse_mode="html")

    if message.from_user.id in ADMINS:
        b1 = types.KeyboardButton("Ro'yxatdan o'tganlar📃")
        b2 = types.KeyboardButton("Savol va takliflar📝")
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(b1,b2)
        await message.reply(f"Salom, ADMIN {message.from_user.first_name}❗Nima xohlaysiz?😊",parse_mode="HTML",reply_markup=keyboard)
    else:

        if await is_subscribed(message.from_user.id) == True and message.from_user.id in user_ids_list:
            keyboard = InlineKeyboardMarkup(row_width=1)
            keyboard.add(InlineKeyboardButton("Savol yoki takliflar📫", callback_data="suggest"))
            await message.answer(f"Assalom alekum hurmatli {message.from_user.full_name}😊Qandaydir taklif va savollaringiz bo'lsa, ushbu tugamachani bosing va fikringizni yozib qoldiring.Taklif va savollar cheklanmagan📫",reply_markup=keyboard)
        elif await is_subscribed(message.from_user.id) == True and message.from_user.id not in user_ids_list:
            keyboard = InlineKeyboardMarkup(row_width=1)
            keyboard.add(InlineKeyboardButton("Ro'yxatdan o'tish🏷️", callback_data="register"))
            keyboard.add(InlineKeyboardButton("Savol yoki takliflar📫", callback_data="suggest"))
            await message.answer(f"Assalom alekum hurmatli {message.from_user.full_name}😊Qandaydir taklif va savollaringiz bo'lsa, ushbu tugamachani bosing va fikringizni yozib qoldiring.Taklif va savollar cheklanmagan📫\nYoki texnikumimizga ro'yxatdan o'ting",reply_markup=keyboard)
        else:
            keyboard = InlineKeyboardMarkup(row_width=1)
            for username, name in CHANNELS.items():
                keyboard.add(InlineKeyboardButton(f"✅ {name}", url=f"https://t.me/{username}"))

            keyboard.add(InlineKeyboardButton("🔄 Tekshirish", callback_data="check_sub"))

            await message.answer(
                "❌ Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling(Eslatma agarda ro'yxatdan o'tish paytida kanalni tark etsangiz, ma'lumotlaringiz o'chib qaytadan ro'yxatdan o'tishingizga to'g'ri keladi):",
                reply_markup=keyboard
            )

@dp.message_handler(Text(equals="Ro'yxatdan o'tganlar📃", ignore_case=True))
async def handle_option1(message: types.Message):
    csv_to_excel("registered_users.csv","registered_users.xlsx")
    with open("registered_users.xlsx", "rb") as file:
        await bot.send_document(
            chat_id=message.chat.id,
            document=file,
            caption="📄 Bu sizning ro'yxatdan o'tgan foydalanuvchilaringizning excel formatdagi fayli."
        )
    csv_to_pdf("registered_users.csv","registered_users.pdf")
    with open("registered_users.pdf", "rb") as file:
        await bot.send_document(
            chat_id=message.chat.id,
            document=file,
            caption="📄 Bu sizning ro'yxatdan o'tgan foydalanuvchilaringiz pdf formatdagi fayli."
        )


"""SAVOL VA TAKLIFLAR QISMI"""

class AnswerState(StatesGroup):
    waiting_for_answer = State()

def load_data_suggest():
    try:
        with open("suggests.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        return sorted(data, key=lambda x: x["date"])
    except:
        return False
def save_data_suggest(data):
    with open("suggests.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def create_inline_keyboard_suggest():

    keyboard = InlineKeyboardMarkup(row_width=1)
    data = load_data_suggest()
    for idx, item in enumerate(data, start=1):
        button = InlineKeyboardButton(
            text=f"{idx}. {item['date']}", callback_data=f"suggest_{idx}"
        )
        keyboard.add(button)
    if keyboard:
        return keyboard
    else:
        return False

@dp.message_handler(Text(equals="Savol va takliflar📝", ignore_case=True))
async def handle_option1(message: types.Message):
    keyboard = create_inline_keyboard_suggest()
    if keyboard==False:
        await message.reply(text="Afsuski hech kim hali taklif yubormagan🥲")
    else:
        await message.answer("📌 Takliflar ro‘yxati:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith("suggest_"))
async def process_suggestion(callback_query: types.CallbackQuery):
    idx = int(callback_query.data.split("_")[1]) - 1
    data = load_data_suggest()
    if 0 <= idx < len(data):
        item = data[idx]
        text = (f"📅 Sana: {item['date']}\n"
                f'👤 Foydalanuvchi id: <a href="tg://user?id={item["user_id"]}">{item["user_id"]}</a>'
                f"👤 Foydalanuvchi: {item['name']} (@{item['username']})\n"
                f"📝 Taklif:\n{item['suggest']}")

        reply_button = InlineKeyboardMarkup(row_width=1)
        reply_button.add(
            InlineKeyboardButton("✍️ Javob yozish", callback_data=f"answer_to_{item['date']}"),
            InlineKeyboardButton("⬅️ Ortga", callback_data="back_to_list")
        )
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=text,
            reply_markup=reply_button,parse_mode="html"
        )

    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data.startswith("answer_to_"))
async def start_answering(callback_query: types.CallbackQuery, state: FSMContext):
    date = callback_query.data.split("_")[2]
    await state.update_data(selected_date=date)

    await bot.send_message(
        callback_query.message.chat.id,
        "✍️ Javobingizni yozing:"
    )
    await AnswerState.waiting_for_answer.set()

    await bot.answer_callback_query(callback_query.id)


# Javobni qabul qilish va foydalanuvchiga jo‘natish
@dp.message_handler(state=AnswerState.waiting_for_answer)
async def send_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    selected_date = data.get("selected_date")

    suggests = load_data_suggest()
    suggestion = next((s for s in suggests if s["date"] == selected_date), None)

    if not suggestion:
        await message.answer("❌ Taklif topilmadi.")
        await state.finish()
        return

    user_id = suggestion["user_id"]
    answer_text = message.text

    try:
        # Foydalanuvchiga javobni jo‘natish
        await bot.send_message(
            user_id,
            f"📬 Sizning taklifingizga javob keldi!\n\n"
            f"📅 Sana: {suggestion['date']}\n"
            f"📝 Taklif: {suggestion['suggest']}\n\n"
            f"✅ Javob: {answer_text}"
        )

        # Taklifni JSON dan o‘chirish
        suggests = [s for s in suggests if s["date"] != selected_date]
        save_data_suggest(suggests)

        await message.answer("✅ Javob yuborildi va taklif ro‘yxatdan o‘chirildi.")

    except Exception as e:
        await message.answer("⚠️ Bu foydalanuvchi botni bloklagan yoki unga xabar yuborib bo‘lmaydi.")

    await state.finish()


@dp.callback_query_handler(lambda c: c.data == "back_to_list")
async def back_to_list(callback_query: types.CallbackQuery):
    keyboard = create_inline_keyboard_suggest()

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text="📌 Takliflar ro‘yxati:",
        reply_markup=keyboard
    )


@dp.message_handler(Command(["start", "stop"]), state="*")
async def cancel_form(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("🚫 Forma to‘xtatildi. Qaytadan boshlash uchun /start ni bosing.", reply_markup=types.ReplyKeyboardRemove())
@dp.message_handler(lambda message: message.text.startswith("/"), state="*")
async def block_commands_during_form(message: types.Message):
    await message.reply("❌ Siz hozir formani to‘ldiryapsiz. Uni yakunlash yoki bekor qilish uchun /stop ni bosing.Yoki to'ldirishda davom eting!")

@dp.callback_query_handler(lambda c: c.data.startswith("suggest"))
async def register_start(callback: types.CallbackQuery,state:FSMContext):
    if await is_subscribed(callback.from_user.id) == True:
        await callback.message.edit_text("Iltimos fikrlaringzni aniq tushunarli bayon eting va botni tark etmang.Adminlarimiz ushbu savol yoki taklifingizga 12 soat ichida javob berishga harkat qilishadi😊.Marhamat yozishingiz mumkin📝")
        await SuggestState.suggest.set()
    else:
        await state.finish()
        await state.reset_state(with_data=True)
        keyboard = InlineKeyboardMarkup(row_width=1)
        for username, name in CHANNELS.items():
            keyboard.add(InlineKeyboardButton(f"✅ {name}", url=f"https://t.me/{username}"))

        keyboard.add(InlineKeyboardButton("🔄 Tekshirish", callback_data="check_sub"))

        await callback.message.edit_text(
            "❌ Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling(Eslatma agarda ro'yxatdan o'tish paytida kanalni tark etsangiz, ma'lumotlaringiz o'chib qaytadan ro'yxatdan o'tishingizga to'g'ri keladi):",
            reply_markup=keyboard
        )
@dp.message_handler(state=SuggestState.suggest)
async def suggest(message:types.Message,state:FSMContext):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("Yana savollarim bor📫", callback_data="suggest"))
    telegram_time = message.date
    formatted_time = telegram_time.strftime("%Y-%m-%d %H:%M:%S")
    await state.update_data(user_id=message.from_user.id,username=message.from_user.username, name=message.from_user.full_name,suggest=message.text,date=formatted_time)
    await message.reply("Biz buni qabul qildik, taklif va savollar uchun raxmat.Adminlar tez orada bot orqali sizga javob berishadi📲😊",reply_markup=keyboard)
    data=await state.get_data()
    await state.finish()
    file_path = "suggests.json"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                suggestions = json.load(file)
            except json.JSONDecodeError:
                suggestions = []
    else:
        suggestions = []
    suggestions.append(data)

    # Write back to file
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(suggestions, file, ensure_ascii=False, indent=4)
    await notify_admins("<strong>Sizga yangi taklif yoki savol yuborildi📝ADMIIIIIIIN😵</strong>")
    await notify_admins(
                f"<a href='tg://user?id={data['user_id']}'>Yuboruvchi Telegram id: [{data['user_id']}]</a>"
                f"\n<a href='https://t.me/{data['username']}'>Yuboruvchi Telegram username: [{data['username']}]</a>"
                f"\nYuboruvchi Telegram nickname: <strong>{data['name']}</strong>\n"
                f"\n━━━━━━━━━━━━━━━━━━━━━━\n"
                f"<strong>🌟 TAKLIF YOKI SAVOL 🌟</strong>\n"
                f"📝 {data['suggest']}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━"
                f"\n📅Yuborilgan sana:{data['date']}"
                )
@dp.callback_query_handler(lambda c: c.data.startswith("register"))
async def register_start(callback: types.CallbackQuery,state:FSMContext):
    user_ids=get_user_ids()
    if await is_subscribed(callback.from_user.id)==True:
        if callback.from_user.id not in user_ids:
            inlines = await major_keyboard()
            if callback.from_user.id in ADMINS:
                await callback.message.answer(f"Salom, ADMIN {callback.from_user.first_name}❗Nima xohlaysiz?😊", parse_mode="HTML")
            else:
                if inlines.inline_keyboard:  # ✅ Prevents sending empty keyboards
                    await callback.message.answer(
                        f"Salom, {callback.from_user.first_name}❗Iltimos ro'yxatdan o'tish uchun pastdagi yo'nalishlardan birini tanlang👇(Ro'yxatdan o'tishni to'xtatish uchun /stop buyrug'ini bosing)",
                        parse_mode="HTML",
                        reply_markup=inlines
                    )
                    await RegisterStates.major.set()
        else:
            keyboard = InlineKeyboardMarkup(row_width=1)
            keyboard.add(InlineKeyboardButton("Savol yoki takliflar📫", callback_data="suggest"))
            await callback.message.edit_text(
                f"Siz allaqchon ro'yxatdan o'tgansiz😊Qandaydir taklif va savollaringiz bo'lsa, ushbu tugamachani bosing va fikringizni yozib qoldiring.Taklif va savollar cheklanmagan📫",
                reply_markup=keyboard)
    else:
        await state.finish()
        await state.reset_state(with_data=True)
        keyboard = InlineKeyboardMarkup(row_width=1)
        for username, name in CHANNELS.items():
            keyboard.add(InlineKeyboardButton(f"✅ {name}", url=f"https://t.me/{username}"))

        keyboard.add(InlineKeyboardButton("🔄 Tekshirish", callback_data="check_sub"))

        await callback.message.edit_text(
            "❌ Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling(Eslatma agarda ro'yxatdan o'tish paytida kanalni tark etsangiz, ma'lumotlaringiz o'chib qaytadan ro'yxatdan o'tishingizga to'g'ri keladi):",
            reply_markup=keyboard
        )
async def major_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    majors = get_majors()

    if not majors:
        return keyboard  # ✅ Prevents errors if API returns no courses

    for index, major in enumerate(majors):
        short_key = f"course_{index}"
        keyboard.add(types.InlineKeyboardButton(text=major, callback_data=short_key))

    return keyboard


@dp.callback_query_handler(lambda c: c.data.startswith("course_"), state=RegisterStates.major)
async def choose_major(callback: types.CallbackQuery, state: FSMContext):
    if await is_subscribed(callback.from_user.id) == True:
        data = await state.get_data()
        if data.get('user_id') == callback.from_user.id:
            index = int(callback.data.split("_")[1])
            majors = get_majors()

            if index >= len(majors):
                await callback.answer("Xatolik! Kurs topilmadi.", show_alert=True)
                return

            major = majors[index]
            await state.update_data(major=major)
            await check_class_call(callback,state)

        else:
            index = int(callback.data.split("_")[1])
            majors = get_majors()

            if index >= len(majors):
                await callback.answer("Xatolik! Kurs topilmadi.", show_alert=True)
                return

            major = majors[index]
            await state.update_data(
                major=major
            )

            await callback.message.edit_text(f"🔹 Siz tanladingiz: {major}\n\n👤 Ismingizni to'liq kiriting:")
            await RegisterStates.full_name.set()
    else:
        await state.finish()
        await state.reset_state(with_data=True)
        keyboard = InlineKeyboardMarkup(row_width=1)
        for username, name in CHANNELS.items():
            keyboard.add(InlineKeyboardButton(f"✅ {name}", url=f"https://t.me/{username}"))

        keyboard.add(InlineKeyboardButton("🔄 Tekshirish", callback_data="check_sub"))

        await callback.message.answer(
            "❌ Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling(Eslatma agarda ro'yxatdan o'tish paytida kanalni tark etsangiz, ma'lumotlaringiz o'chib qaytadan ro'yxatdan o'tishingizga to'g'ri keladi):",
            reply_markup=keyboard
        )
@dp.message_handler(state=RegisterStates.full_name)
async def enter_full_name(message: types.Message, state: FSMContext):
    if await is_subscribed(message.from_user.id) == True:
        data=await state.get_data()
        print(data)
        if data.get('user_id')==message.from_user.id:
            print("eded")
            await state.update_data(name=message.text)
            await check_class(message,state)
        else:
            print("yoqq")
            await state.update_data(name=message.text)
            await message.reply(f"🔢Yoshingizni kiriting:")
            await RegisterStates.age.set()
    else:
        await state.finish()
        await state.reset_state(with_data=True)
        keyboard = InlineKeyboardMarkup(row_width=1)
        for username, name in CHANNELS.items():
            keyboard.add(InlineKeyboardButton(f"✅ {name}", url=f"https://t.me/{username}"))

        keyboard.add(InlineKeyboardButton("🔄 Tekshirish", callback_data="check_sub"))

        await message.answer(
                        "❌ Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling(Eslatma agarda ro'yxatdan o'tish paytida kanalni tark etsangiz, ma'lumotlaringiz o'chib qaytadan ro'yxatdan o'tishingizga to'g'ri keladi):",
            reply_markup=keyboard
        )
@dp.message_handler(lambda message: not message.text.isdigit(), state=RegisterStates.age)
async def invalid_age(message: types.Message):
    await message.reply("❌ Iltimos, yoshingizni faqat raqam bilan kiriting!")

@dp.message_handler(lambda message: message.text.isdigit(), state=RegisterStates.age)
async def enter_age(message: types.Message, state: FSMContext):
    if await is_subscribed(message.from_user.id) == True:
        await state.update_data(age=int(message.text))
        data = await state.get_data()
        if data.get('user_id') == message.from_user.id:
            await state.update_data(age=message.text)
            await check_class(message, state)
        else:
            await message.reply(f"📍 Viloyat/tumaningizni kiriting masalan:\n<i>Toshkent viloyati Parkent tumani</i>", parse_mode="html")
            await RegisterStates.location.set()
    else:
        await state.finish()
        await state.reset_state(with_data=True)
        keyboard = InlineKeyboardMarkup(row_width=1)
        for username, name in CHANNELS.items():
            keyboard.add(InlineKeyboardButton(f"✅ {name}", url=f"https://t.me/{username}"))

        keyboard.add(InlineKeyboardButton("🔄 Tekshirish", callback_data="check_sub"))

        await message.answer(
            "❌ Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling(Eslatma agarda ro'yxatdan o'tish paytida kanalni tark etsangiz, ma'lumotlaringiz o'chib qaytadan ro'yxatdan o'tishingizga to'g'ri keladi):",
            reply_markup=keyboard
        )

import re


@dp.message_handler(state=RegisterStates.location)
async def enter_location(message: types.Message, state: FSMContext):
    if await is_subscribed(message.from_user.id) == True:
        data = await state.get_data()
        if data.get('user_id') == message.from_user.id:
            await state.update_data(location=message.text)
            await check_class(message, state)
        else:
            await state.update_data(location=message.text)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            contact_button = types.KeyboardButton("📞 Raqamni ulashish", request_contact=True)
            keyboard.add(contact_button)

            await message.reply("📱 Telefon raqamingizni kiriting yoki pastdagi tugmani bosing:", reply_markup=keyboard)
            await RegisterStates.phone.set()
    else:
        await state.finish()
        await state.reset_state(with_data=True)
        keyboard = InlineKeyboardMarkup(row_width=1)
        for username, name in CHANNELS.items():
            keyboard.add(InlineKeyboardButton(f"✅ {name}", url=f"https://t.me/{username}"))

        keyboard.add(InlineKeyboardButton("🔄 Tekshirish", callback_data="check_sub"))

        await message.answer(
            "❌ Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling(Eslatma agarda ro'yxatdan o'tish paytida kanalni tark etsangiz, ma'lumotlaringiz o'chib qaytadan ro'yxatdan o'tishingizga to'g'ri keladi):",
            reply_markup=keyboard
        )

@dp.message_handler(content_types=types.ContentType.CONTACT, state=RegisterStates.phone)
async def process_contact(message: types.Message, state: FSMContext):
    if await is_subscribed(message.from_user.id) == True:
        data=await state.get_data()

        if data.get('user_id') == message.from_user.id:
            if message.contact:
                phone_number = message.contact.phone_number
                await state.update_data(phone=phone_number)
                await message.reply("✅ Raqamingiz qabul qilindi.", reply_markup=types.ReplyKeyboardRemove())
                await check_class(message, state)
        else:
            if message.contact:
                phone_number = message.contact.phone_number
                await state.update_data(phone=phone_number)
                await message.reply("✅ Raqamingiz qabul qilindi.", reply_markup=types.ReplyKeyboardRemove())
                await send_class_selection(message)
                await RegisterStates.student_class.set()
    else:
        await state.finish()
        await state.reset_state(with_data=True)
        keyboard = InlineKeyboardMarkup(row_width=1)
        for username, name in CHANNELS.items():
            keyboard.add(InlineKeyboardButton(f"✅ {name}", url=f"https://t.me/{username}"))

        keyboard.add(InlineKeyboardButton("🔄 Tekshirish", callback_data="check_sub"))

        await message.answer(
            "❌ Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling(Eslatma agarda ro'yxatdan o'tish paytida kanalni tark etsangiz, ma'lumotlaringiz o'chib qaytadan ro'yxatdan o'tishingizga to'g'ri keladi):",
            reply_markup=keyboard
        )

@dp.message_handler(state=RegisterStates.phone)
async def process_manual_phone(message: types.Message, state: FSMContext):
    if await is_subscribed(message.from_user.id) == True:
        data = await state.get_data()
        if data.get('user_id') == message.from_user.id:
            phone_regex = r"^\+998[0-9]{9}$"  # Uzbekistan raqam formati
            if not re.match(phone_regex, message.text):
                await message.reply(
                    "❌ Noto‘g‘ri raqam formati! Raqamni +998XXXXXXXXX shaklida kiriting yoki tugmadan foydalaning.")
                return

            await state.update_data(phone=message.text)
            await message.reply("✅ Raqamingiz qabul qilindi.", reply_markup=types.ReplyKeyboardRemove())
            await check_class(message, state)
        else:
            phone_regex = r"^\+998[0-9]{9}$"  # Uzbekistan raqam formati
            if not re.match(phone_regex, message.text):
                await message.reply(
                    "❌ Noto‘g‘ri raqam formati! Raqamni +998XXXXXXXXX shaklida kiriting yoki tugmadan foydalaning.")
                return

            await state.update_data(phone=message.text)
            await message.reply("✅ Raqamingiz qabul qilindi.", reply_markup=types.ReplyKeyboardRemove())
            await send_class_selection(message)
            await RegisterStates.student_class.set()
    else:
        await state.finish()
        await state.reset_state(with_data=True)
        keyboard = InlineKeyboardMarkup(row_width=1)
        for username, name in CHANNELS.items():
            keyboard.add(InlineKeyboardButton(f"✅ {name}", url=f"https://t.me/{username}"))

        keyboard.add(InlineKeyboardButton("🔄 Tekshirish", callback_data="check_sub"))

        await message.answer(
            "❌ Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling(Eslatma agarda ro'yxatdan o'tish paytida kanalni tark etsangiz, ma'lumotlaringiz o'chib qaytadan ro'yxatdan o'tishingizga to'g'ri keladi):",
            reply_markup=keyboard
        )


async def send_class_selection(message: types.Message):
    """ Inline tugmalar bilan 9-sinf va 11-sinf tanlashni jo‘natish """
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="📘 9-sinf", callback_data="class_9"),
        InlineKeyboardButton(text="📗 11-sinf", callback_data="class_11")
    )

    await message.answer("📚 Bitiruvchi sinfni tanlang:", reply_markup=keyboard)
async def send_system_selection(callback: types.CallbackQuery):
    """ Inline tugmalar bilan ta'lim shaklini tanlashni jo‘natish """
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="📚 Sirtqi", callback_data="system_Sirtqi"),
        InlineKeyboardButton(text="☀️ Kunduzgi", callback_data="system_Kunduzgi"),
        InlineKeyboardButton(text="⚡ Dual", callback_data="system_Dual")
    )

    await callback.message.answer("📖 Ta'lim shaklini tanlang:", reply_markup=keyboard)
async def get_edit_keyboard(student_class):
    keyboard = InlineKeyboardMarkup(row_width=3)

    buttons = [
        InlineKeyboardButton("1️⃣", callback_data="edit_major"),
        InlineKeyboardButton("2️⃣", callback_data="edit_name"),
        InlineKeyboardButton("3️⃣", callback_data="edit_age"),
        InlineKeyboardButton("4️⃣", callback_data="edit_location"),
        InlineKeyboardButton("5️⃣", callback_data="edit_phone"),
        InlineKeyboardButton("6️⃣", callback_data="edit_student_class"),
    ]

    if student_class == "11":
        buttons.append(InlineKeyboardButton("7️⃣", callback_data="edit_system"))  # 11-sinf uchun qo‘shiladi

    buttons.append(InlineKeyboardButton("✅ Tasdiqlash", callback_data="confirm"))

    keyboard.add(*buttons)
    return keyboard
@dp.callback_query_handler(lambda c: c.data.startswith("class_"), state=RegisterStates.student_class)
async def process_class_selection(callback: types.CallbackQuery, state: FSMContext):
    if await is_subscribed(callback.from_user.id) ==True:
        data=await state.get_data()
        if data.get('user_id')==callback.from_user.id:
            selected_class = callback.data.split("_")[1]
            if data.get("student_class") == "9" and selected_class=="11":
                await state.update_data(student_class=selected_class)
                await send_system_selection(callback)
                await RegisterStates.system.set()
            if data.get("student_class")=="11" and selected_class=="9":
                del data['system']
                await state.set_data(data)
                await state.update_data(student_class=selected_class)
                await check_class_call(callback,state)
            else:
                await state.update_data(student_class=selected_class)
                await check_class_call(callback, state)

        else:
            selected_class = callback.data.split("_")[1]  # "9" yoki "11"
            await state.update_data(student_class=selected_class,user_id = callback.from_user.id, username = callback.from_user.username)

            await callback.message.edit_text(f"✅ Siz {selected_class}-sinfni tanladingiz!")
            await callback.answer()

            if selected_class == "11":
                await send_system_selection(callback)
                await RegisterStates.system.set()
            if selected_class == "9":
                data=await state.get_data()
                await callback.message.answer(
                    "❗Yaxshi endi ma'lumotlaringiz to'g'riligini tekshiring:\n"
                    f"\n<strong>1.</strong>📖 Yo'nalishingiz: <strong>{data['major']}</strong>"
                    f"\n<strong>2.</strong>📄Ism-familiya: <strong>{data['name']}</strong>"
                    f"\n<strong>3.</strong>🔢Yosh: <strong>{data['age']}</strong>"
                    f"\n<strong>4.</strong>📍Manzil: <i>{data['location']}</i>"
                    f"\n<strong>5.</strong>📲Telefon raqam: <strong>{data['phone']}</strong>"
                    f"\n<strong>6.</strong>📚Sinf: <strong>{data['student_class']}</strong>"
                   ,parse_mode="html",reply_markup=await get_edit_keyboard(selected_class))
                await RegisterStates.confirm.set()
    else:
        await state.finish()
        await state.reset_state(with_data=True)
        keyboard = InlineKeyboardMarkup(row_width=1)
        for username, name in CHANNELS.items():
            keyboard.add(InlineKeyboardButton(f"✅ {name}", url=f"https://t.me/{username}"))

        keyboard.add(InlineKeyboardButton("🔄 Tekshirish", callback_data="check_sub"))

        await callback.message.answer(
            "❌ Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling(Eslatma agarda ro'yxatdan o'tish paytida kanalni tark etsangiz, ma'lumotlaringiz o'chib qaytadan ro'yxatdan o'tishingizga to'g'ri keladi):",
            reply_markup=keyboard
        )
async def check_class_call(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    student_class = data.get('student_class')

    if student_class == "9":
        await callback.message.edit_text(
            "❗Yaxshi endi ma'lumotlaringiz to'g'riligini tekshiring:\n"
            f"\n<strong>1.</strong>📖 Yo'nalishingiz: <strong>{data['major']}</strong>"
            f"\n<strong>2.</strong>📄Ism-familiya: <strong>{data['name']}</strong>"
            f"\n<strong>3.</strong>🔢Yosh: <strong>{data['age']}</strong>"
            f"\n<strong>4.</strong>📍Manzil: <i>{data['location']}</i>"
            f"\n<strong>5.</strong>📲Telefon raqam: <strong>{data['phone']}</strong>"
            f"\n<strong>6.</strong>📚Sinf: <strong>{data['student_class']}</strong>"
           , parse_mode="html", reply_markup=await get_edit_keyboard(student_class))
        await RegisterStates.confirm.set()
    if student_class == "11":
        await callback.message.edit_text(
            f"✅❗Yaxshi endi ma'lumotlaringiz to'g'riligini tekshiring:\n"
            f"\n<strong>1.</strong>📖 Yo'nalishingiz: <strong>{data['major']}</strong>"
            f"\n<strong>2.</strong>📄Ism-familiya: <strong>{data['name']}</strong>"
            f"\n<strong>3.</strong>🔢Yosh: <strong>{data['age']}</strong>"
            f"\n<strong>4.</strong>📍Manzil: <i>{data['location']}</i>"
            f"\n<strong>5.</strong>📲Telefon raqam: <strong>{data['phone']}</strong>"
            f"\n<strong>6.</strong>📚Sinf: <strong>{data['student_class']}</strong>"
            f"\n<strong>7.</strong>📖 Ta'lim shakli: <strong>{data['system']}</strong>", parse_mode="html",
            reply_markup=await get_edit_keyboard(student_class))
        await RegisterStates.confirm.set()

async def check_class(message:types.Message,state:FSMContext):
    data=await state.get_data()
    student_class=data.get('student_class')

    if student_class=="9":
        await message.answer(
            "❗Yaxshi endi ma'lumotlaringiz to'g'riligini tekshiring:\n"
            f"\n<strong>1.</strong>📖 Yo'nalishingiz: <strong>{data['major']}</strong>"
            f"\n<strong>2.</strong>📄Ism-familiya: <strong>{data['name']}</strong>"
            f"\n<strong>3.</strong>🔢Yosh: <strong>{data['age']}</strong>"
            f"\n<strong>4.</strong>📍Manzil: <i>{data['location']}</i>"
            f"\n<strong>5.</strong>📲Telefon raqam: <strong>{data['phone']}</strong>"
            f"\n<strong>6.</strong>📚Sinf: <strong>{data['student_class']}</strong>"
           ,parse_mode="html",reply_markup=await get_edit_keyboard(student_class))
        await RegisterStates.confirm.set()
    if student_class=="11":
        await message.answer(
            f"✅❗Yaxshi endi ma'lumotlaringiz to'g'riligini tekshiring:\n"
            f"\n<strong>1.</strong>📖 Yo'nalishingiz: <strong>{data['major']}</strong>"
            f"\n<strong>2.</strong>📄Ism-familiya: <strong>{data['name']}</strong>"
            f"\n<strong>3.</strong>🔢Yosh: <strong>{data['age']}</strong>"
            f"\n<strong>4.</strong>📍Manzil: <i>{data['location']}</i>"
            f"\n<strong>5.</strong>📲Telefon raqam: <strong>{data['phone']}</strong>"
            f"\n<strong>6.</strong>📚Sinf: <strong>{data['student_class']}</strong>"
            f"\n<strong>7.</strong>📖 Ta'lim shakli: <strong>{data['system']}</strong>", parse_mode="html",
            reply_markup=await get_edit_keyboard(student_class))
        await RegisterStates.confirm.set()

@dp.callback_query_handler(lambda c: c.data.startswith("system_"), state=RegisterStates.system)
async def process_system_selection(callback: types.CallbackQuery,state:FSMContext):
    if await is_subscribed(callback.from_user.id) == True:
        data = await state.get_data()
        if data.get('user_id')==callback.from_user.id:
            selected_system = callback.data.split("_")[1]
            await state.update_data(system=selected_system)
            await check_class_call(callback,state)
        else:
            selected_system=callback.data.split("_")[1]
            await state.update_data(system=selected_system,user_id = callback.from_user.id, username = callback.from_user.username)
            student_class = data.get('student_class', '9')
            await callback.message.edit_text(f"✅ Siz <strong>{selected_system}</strong> talim shaklini tanladingiz❗Yaxshi endi ma'lumotlaringiz to'g'riligini tekshiring:\n"
                                             f"\n<strong>1.</strong>📖 Yo'nalishingiz: <strong>{data['major']}</strong>"
                                             f"\n<strong>2.</strong>📄Ism-familiya: <strong>{data['name']}</strong>"
                                             f"\n<strong>3.</strong>🔢Yosh: <strong>{data['age']}</strong>"
                                             f"\n<strong>4.</strong>📍Manzil: <i>{data['location']}</i>"
                                             f"\n<strong>5.</strong>📲Telefon raqam: <strong>{data['phone']}</strong>"
                                             f"\n<strong>6.</strong>📚Sinf: <strong>{data['student_class']}</strong>"
                                             f"\n<strong>7.</strong>📖 Ta'lim shakli: <strong>{data['system']}</strong>",parse_mode="html",reply_markup=await get_edit_keyboard(student_class))

            await RegisterStates.confirm.set()
    else:
        await state.finish()
        await state.reset_state(with_data=True)
        keyboard = InlineKeyboardMarkup(row_width=1)
        for username, name in CHANNELS.items():
            keyboard.add(InlineKeyboardButton(f"✅ {name}", url=f"https://t.me/{username}"))

        keyboard.add(InlineKeyboardButton("🔄 Tekshirish", callback_data="check_sub"))

        await callback.message.answer(
            "❌ Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling(Eslatma agarda ro'yxatdan o'tish paytida kanalni tark etsangiz, ma'lumotlaringiz o'chib qaytadan ro'yxatdan o'tishingizga to'g'ri keladi):",
            reply_markup=keyboard
        )

@dp.callback_query_handler(lambda c: c.data.startswith("edit_major"),state=RegisterStates.confirm)
async def edit_major(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    inlines = await major_keyboard()

    if inlines.inline_keyboard:
        await callback_query.message.edit_text(
            "📝 Yangi yo‘nalishni tanlang:",
            reply_markup=inlines
        )
        await RegisterStates.major.set()
    else:
        await callback_query.message.answer("⚠️ Hozircha kurslar mavjud emas. Keyinroq urinib ko'ring.")

@dp.callback_query_handler(lambda c: c.data.startswith("edit_name"), state=RegisterStates.confirm)
async def edit_name(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.edit_text("👤 Iltimos, ismingizni qayta kiriting:")
    await RegisterStates.full_name.set()

@dp.callback_query_handler(lambda c: c.data.startswith("edit_age"), state=RegisterStates.confirm)
async def edit_age(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.edit_text("🔢 Iltimos, yoshingizni qayta kiriting:")
    await RegisterStates.age.set()

@dp.callback_query_handler(lambda c: c.data.startswith("edit_location"), state=RegisterStates.confirm)
async def edit_location(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.edit_text("📍 Iltimos, manzilni qayta kiriting:")
    await RegisterStates.location.set()

@dp.callback_query_handler(lambda c: c.data.startswith("edit_phone"), state=RegisterStates.confirm)
async def edit_phone(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    contact_button = types.KeyboardButton("📞 Raqamni ulashish", request_contact=True)
    keyboard.add(contact_button)
    await callback_query.message.delete()
    await callback_query.message.answer(
        "📱 Telefon raqamingizni kiriting yoki pastdagi tugmani bosing:",
        reply_markup=keyboard
    )
    await RegisterStates.phone.set()
@dp.callback_query_handler(lambda c: c.data.startswith("edit_student_class"), state=RegisterStates.confirm)
async def edit_st_class(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.delete()
    data=await state.get_data()
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="📘 9-sinf", callback_data="class_9"),
        InlineKeyboardButton(text="📗 11-sinf", callback_data="class_11")
    )

    await callback_query.message.answer("📚 Bitiruvchi sinfni tanlang:", reply_markup=keyboard)
    await RegisterStates.student_class.set()

@dp.callback_query_handler(lambda c: c.data.startswith("edit_system"), state=RegisterStates.confirm)
async def edit_system(callback_query: types.CallbackQuery, state: FSMContext):

    await callback_query.answer()
    await callback_query.message.delete()
    await send_system_selection(callback_query)
    await RegisterStates.system.set()

import csv
import os
@dp.callback_query_handler(lambda c: c.data.startswith("confirm"), state=RegisterStates.confirm)
async def confirm(callback_query: types.CallbackQuery, state: FSMContext):
    if await is_subscribed(callback_query.from_user.id) == True:
        data=await state.get_data()
        await callback_query.answer()
        await state.finish()
        file_path = "registered_users.csv"
        file_exists = os.path.isfile(file_path)

        # 📌 Ma'lumotlarni CSV faylga yozish uchun funksiya
        def save_to_csv(data):
            with open(file_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(
                        ["ID", "Username", "Ism", "Yosh", "Manzil", "Telefon", "Sinf", "Yo'nalish", "Ta'lim shakli"])

                row = [
                    data['user_id'],
                    data['username'],
                    data['name'],
                    data['age'],
                    data['location'],
                    data['phone'],
                    data['student_class'],
                    data['major'],
                    data.get('system', "Noma'lum")
                ]
                writer.writerow(row)
        save_to_csv(data)
        if data['student_class'] == "9":
            await notify_admins("<strong>Yangi maktab o'quvchisi ro'yxatdan o'tdi</strong>")
            await notify_admins(
                f"<a href='tg://user?id={data['user_id']}'>Telegram id: [{data['user_id']}]</a>"
                f"\n<a href='https://t.me/{data['username']}'>Telegram username: [{data['username']}]</a>\n"
                f"\n<strong>1.</strong>📖 Yo'nalish: <strong>{data['major']}</strong>"
                f"\n<strong>2.</strong>📄Ism-familiya: <strong>{data['name']}</strong>"
                f"\n<strong>3.</strong>🔢Yosh: <strong>{data['age']}</strong>"
                f"\n<strong>4.</strong>📍Manzil: <i>{data['location']}</i>"
                f"\n<strong>5.</strong>📲Telefon raqam: <strong>{data['phone']}</strong>"
                f"\n<strong>6.</strong>📚Sinf: <strong>{data['student_class']}</strong>"
                )
            keyboard = InlineKeyboardMarkup(row_width=1)
            keyboard.add(InlineKeyboardButton("Savol yoki takliflar📫", callback_data="suggest"))
            await bot.send_message(chat_id=data['user_id'], text="<strong>Tabriklaymiz🎉Siz muvaffaqiytali ro'yxatdan o'tdingiz tez orada adminlarimz siz bilan aloqaga chiqadi📲Qandaydir taklif va savollaringiz bo'lsa, ushbu tugamachani bosing va fikringizni yozib qoldiring.Taklif va savollar cheklanmagan📫</strong>",parse_mode="html",reply_markup=keyboard)
        if data['student_class'] == "11":
            await notify_admins("<strong>Yangi odam ro'yxatdan o'tdi</strong>")
            await notify_admins(
                f"<a href='tg://user?id={data['user_id']}'>Telegram id: [{data['user_id']}]</a>"
                f"\n<a href='https://t.me/{data['username']}'>Telegram username: [{data['username']}]</a>\n"
                f"\n<strong>1.</strong>📖 Yo'nalish: <strong>{data['major']}</strong>"
                f"\n<strong>2.</strong>📄Ism-familiya: <strong>{data['name']}</strong>"
                f"\n<strong>3.</strong>🔢Yosh: <strong>{data['age']}</strong>"
                f"\n<strong>4.</strong>📍Manzil: <i>{data['location']}</i>"
                f"\n<strong>5.</strong>📲Telefon raqam: <strong>{data['phone']}</strong>"
                f"\n<strong>6.</strong>📚Sinf: <strong>{data['student_class']}</strong>"
                f"\n<strong>7.</strong>📖 Ta'lim shakli: <strong>{data['system']}</strong>")
            keyboard = InlineKeyboardMarkup(row_width=1)
            keyboard.add(InlineKeyboardButton("Savol yoki takliflar📫", callback_data="suggest"))
            await bot.send_message(chat_id=data['user_id'], text="<strong>Tabriklaymiz🎉Siz muvaffaqiytali ro'yxatdan o'tdingiz tez orada adminlarimz siz bilan aloqaga chiqadi📲Qandaydir taklif va savollaringiz bo'lsa, ushbu tugamachani bosing va fikringizni yozib qoldiring.Taklif va savollar cheklanmagan📫</strong>",parse_mode="html",reply_markup=keyboard)




    else:
        await state.finish()
        await state.reset_state(with_data=True)
        keyboard = InlineKeyboardMarkup(row_width=1)
        for username, name in CHANNELS.items():
            keyboard.add(InlineKeyboardButton(f"✅ {name}", url=f"https://t.me/{username}"))

        keyboard.add(InlineKeyboardButton("🔄 Tekshirish", callback_data="check_sub"))

        await callback_query.message.answer(
            "❌ Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling(Eslatma agarda ro'yxatdan o'tish paytida kanalni tark etsangiz, ma'lumotlaringiz o'chib qaytadan ro'yxatdan o'tishingizga to'g'ri keladi):",
            reply_markup=keyboard
        )
@dp.callback_query_handler(lambda call: call.data == "check_sub")
async def check_subscription_callback(call: types.CallbackQuery):
    if await is_subscribed(call.from_user.id)==True:
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(InlineKeyboardButton("Ro'yxatdan o'tish🏷️", callback_data="register"))
        await call.message.answer("✅Rahmat! Siz obuna bo‘ldingiz.Ro'yxatdan o'tish uchun ushbu tugmani bosing👇",reply_markup=keyboard)
        await call.message.delete()
    else:
        await call.answer("❌ Hali ham obuna bo‘lmagansiz!", show_alert=True)
async def notify_admins(message: str):
    for admin_id in ADMINS:
        try:
            await bot.send_message(admin_id, message,parse_mode="html")
        except Exception as e:
            logging.error(f"Failed to notify admin {admin_id}: {e}")

if __name__ == "__main__":
    async def on_startup(dp):
        await set_web_app_button()
        await set_default_commands(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
