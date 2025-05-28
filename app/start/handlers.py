from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from app.start.keyboards import button_get_file
router = Router()

@router.message(Command("start"))
async def admanel(message: Message):
    await message.answer("Этот бот создан для частного пользования."
                         "\n Если в админ то отправьте команду '/admin'"
                         "Если произошли какие-то проблемы, то обратитесь к администраторам",)