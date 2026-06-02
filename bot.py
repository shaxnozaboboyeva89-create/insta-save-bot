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
                    text="📢 Kanalga obuna bo‘ling",
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
        "Videoni yuklash uchun kanalga obuna bo‘ling:",
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
            "format": "mp4/best"
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        video = FSInputFile(filename)

        await callback.message.answer_video(
            video=video,
            caption="✅ Tayyor"
        )

        os.remove(filename)

        await msg.delete()

    except Exception as e:
        await callback.message.answer(
            f"Xatolik:\n{e}"
        )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())