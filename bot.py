import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    FSInputFile
)
from yt_dlp import YoutubeDL

TOKEN = "8951694747:AAHin4ieYfGMF2h48IW0Yg6--ramSosJ8qI"
CHANNEL = "@instagramdanyukla"

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_links = {}

@dp.message(F.text.startswith("https://www.instagram.com"))
async def instagram_link(message: Message):
    user_links[message.from_user.id] = message.text

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 Kanalga qo‘shilish",
                    url="https://t.me/instagramdanyukla"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Obunani tekshirish",
                    callback_data="check_sub"
                )
            ]
        ]
    )

    await message.answer(
        "📥 Instagram Downloader\n\nVideoni yuklash uchun kanalga obuna bo‘ling 👇",
        reply_markup=keyboard
    )

@dp.callback_query(F.data == "check_sub")
async def check_subscription(callback: CallbackQuery):
    try:
        member = await bot.get_chat_member(
            CHANNEL,
            callback.from_user.id
        )

        if member.status not in ["member", "administrator", "creator"]:
            await callback.answer(
                "❌ Avval kanalga obuna bo‘ling",
                show_alert=True
            )
            return

        link = user_links.get(callback.from_user.id)

        if not link:
            await callback.message.answer(
                "Instagram link yuboring."
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
            caption="🎉 Video muvaffaqiyatli yuklandi!"
        )

        if os.path.exists(filename):
            os.remove(filename)

        await msg.delete()

        audio_btn = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🎵 Audio yuklash",
                        callback_data="audio_download"
                    )
                ]
            ]
        )

        await callback.message.answer(
            "🎵 Videoning audiosini ham yuklaysizmi?",
            reply_markup=audio_btn
        )

    except Exception as e:
        await callback.message.answer(
            f"Xatolik:\n{e}"
        )

@dp.callback_query(F.data == "audio_download")
async def download_audio(callback: CallbackQuery):
    try:
        link = user_links.get(callback.from_user.id)

        if not link:
            await callback.message.answer("Link topilmadi.")
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
            caption="🎵 Audio tayyor"
        )

        if os.path.exists(filename):
            os.remove(filename)

        await msg.delete()

    except Exception as e:
        await callback.message.answer(
            f"Audio xatosi:\n{e}"
        )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())