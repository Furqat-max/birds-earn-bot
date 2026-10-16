from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

router = Router()

HELP_TEXT = (
    "ℹ️ <b>Birds Earn boti bo‘yicha qo‘llanma:</b>\n\n"
    "1️⃣ <b>Qushlar sotib olish:</b> Mini ilovaga (Web App) kiring va fermangiz uchun mos VIP darajadagi qushni tanlang.\n"
    "2️⃣ <b>Daromad:</b> Har bir qush sizga doimiy tarzda soatlik foyda keltiradi.\n"
    "3️⃣ <b>Hisobni to‘ldirish va yechish:</b> To‘lovlar USDT (TRC-20, BEP-20) va TON tarmoqlari orqali avtomatik amalga oshiriladi.\n"
    "4️⃣ <b>Referal tizim:</b> Do‘stlaringizni taklif qilib, ularning har bir xarididan qo‘shimcha foiz oling!\n\n"
    "Savollar yoki muammolar bo‘lsa, adminga murojaat qiling."
)

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(HELP_TEXT)

@router.callback_query(F.data == "help_info")
async def cb_help(call: CallbackQuery):
    await call.answer()
    await call.message.answer(HELP_TEXT)
