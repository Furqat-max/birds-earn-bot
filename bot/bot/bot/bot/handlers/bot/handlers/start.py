from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import os
from bot.db_bridge import get_or_create_user

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject):
    referrer_id = None
    args = command.args
    if args and args.isdigit():
        referrer_id = int(args)

    user, created = await get_or_create_user(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        referrer_id=referrer_id
    )

    webapp_url = os.getenv("WEBAPP_URL", "https://t.me")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎮 Fermani ochish (Web App)", 
                    web_app=WebAppInfo(url=webapp_url)
                )
            ],
            [
                InlineKeyboardButton(text="👥 Taklif qilish", callback_data="ref_info"),
                InlineKeyboardButton(text="ℹ️ Yordam", callback_data="help_info")
            ]
        ]
    )

    welcome_text = (
        f"Assalomu alaykum, <b>{message.from_user.first_name}</b>!\n\n"
        f"🦅 <b>Birds Earn</b> virtual qushlar fermasiga xush kelibsiz.\n\n"
        f"🌾 VIP qushlarni sotib oling va har soatda barqaror foyda oling!\n"
        f"O'yinni boshlash uchun quyidagi tugmani bosing 👇"
    )

    await message.answer(welcome_text, reply_markup=keyboard)
