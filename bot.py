import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

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

        if member.status in ["member", "administrator", "creator"]:
            await callback.message.answer(
                "✅ Obuna tasdiqlandi.\n\nKeyingi bosqichda video yuklashni ulaymiz."
            )
        else:
            await callback.answer(
                "❌ Avval kanalga obuna bo‘ling",
                show_alert=True
            )

    except:
        await callback.answer(
            "❌ Avval kanalga obuna bo‘ling",
            show_alert=True
        )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())