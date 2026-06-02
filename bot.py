import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

TOKEN = "TOKENINGIZ"
CHANNEL = "@instagramdanyukla"

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_lang = {}

lang_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")]
    ]
)

menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔗 Link yuborish"),
            KeyboardButton(text="📢 Kanal")
        ],
        [
            KeyboardButton(text="🎵 Audio"),
            KeyboardButton(text="ℹ️ Yordam")
        ]
    ],
    resize_keyboard=True
)

@dp.message(F.text == "/start")
async def start(message: Message):
    await message.answer(
        "👋 Xush kelibsiz!\n\nTilni tanlang:",
        reply_markup=lang_kb
    )

@dp.callback_query(F.data.startswith("lang_"))
async def choose_lang(callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    user_lang[callback.from_user.id] = lang

    await callback.message.answer(
        "📥 InstaSave Bot\n\nKerakli bo‘limni tanlang:",
        reply_markup=menu_kb
    )

@dp.message(F.text == "📢 Kanal")
async def channel_btn(message: Message):
    await message.answer(
        "📢 Kanalimiz:",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🚀 Kanalga o'tish",
                        url="https://t.me/instagramdanyukla"
                    )
                ]
            ]
        )
    )

@dp.message(F.text == "ℹ️ Yordam")
async def help_btn(message: Message):
    await message.answer(
        "📌 Instagram link yuboring.\n"
        "📌 Kanalga obuna bo‘ling.\n"
        "📌 Video yoki audio yuklab oling."
    )user_links = {}

@dp.message(F.text == "🔗 Link yuborish")
async def ask_link(message: Message):
    await message.answer(
        "📎 Instagram linkini yuboring:"
    )

@dp.message(F.text.startswith("https://www.instagram.com"))
async def instagram_link(message: Message):
    user_links[message.from_user.id] = message.text

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Kanalga obuna bo‘lish",
                    url="https://t.me/instagramdanyukla"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Tekshirish",
                    callback_data="check_sub"
                )
            ]
        ]
    )

    await message.answer(
        "📥 Link qabul qilindi.\n\n"
        "Videoni yuklash uchun kanalga obuna bo‘ling 👇",
        reply_markup=keyboard
    )

@dp.callback_query(F.data == "check_sub")
async def check_subscription(callback: CallbackQuery):
    try:
        member = await bot.get_chat_member(
            CHANNEL,
            callback.from_user.id
        )

        if member.status not in [
            "member",
            "administrator",
            "creator"
        ]:
            await callback.answer(
                "❌ Avval kanalga obuna bo‘ling",
                show_alert=True
            )
            return

        choose_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🎬 Videoni yuklash",
                        callback_data="download_video"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🎵 Audioni yuklash",
                        callback_data="download_audio"
                    )
                ]
            ]
        )

        await callback.message.answer(
            "✅ Obuna tasdiqlandi.\n\n"
            "📥 Nima yuklamoqchisiz?",
            reply_markup=choose_kb
        )

    except:
        await callback.answer(
            "❌ Obunani tekshirib bo‘lmadi",
            show_alert=True
        )import os
from aiogram.types import FSInputFile
from yt_dlp import YoutubeDL

@dp.callback_query(F.data == "download_video")
async def download_video(callback: CallbackQuery):
    try:
        link = user_links.get(callback.from_user.id)

        if not link:
            await callback.message.answer(
                "❌ Link topilmadi. Qaytadan yuboring."
            )
            return

        msg = await callback.message.answer(
            "⏳ Video yuklanmoqda..."
        )

        filename = f"{callback.from_user.id}.mp4"

        ydl_opts = {
            "outtmpl": filename,
            "format": "best",
            "socket_timeout": 120
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        video = FSInputFile(filename)

        await callback.message.answer_video(
            video=video,
            caption="🎬 Video tayyor!"
        )

        if os.path.exists(filename):
            os.remove(filename)

        await msg.delete()

    except Exception as e:
        await callback.message.answer(
            f"❌ Video xatosi:\n{e}"
        )@dp.callback_query(F.data == "download_audio")
async def download_audio(callback: CallbackQuery):
    try:
        link = user_links.get(callback.from_user.id)

        if not link:
            await callback.message.answer(
                "❌ Link topilmadi. Qaytadan yuboring."
            )
            return

        msg = await callback.message.answer(
            "🎵 Audio yuklanmoqda..."
        )

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"{callback.from_user.id}.%(ext)s"
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            filename = ydl.prepare_filename(info)

        audio = FSInputFile(filename)

        await callback.message.answer_audio(
            audio=audio,
            caption="🎵 Audio tayyor!"
        )

        if os.path.exists(filename):
            os.remove(filename)

        await msg.delete()

    except Exception as e:
        await callback.message.answer(
            f"❌ Audio xatosi:\n{e}"
        )