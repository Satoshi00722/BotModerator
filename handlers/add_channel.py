from aiogram import Router
from aiogram.types import Message
from database import add_channel

router = Router()

@router.channel_post(lambda m: m.text and m.text.startswith("/add_channel"))
async def add_channel_handler(message: Message):
    chat = message.chat

    # ⚠️ ВАЖНО: username есть только у публичных каналов
    username = chat.username  # может быть None, если канал приватный

    add_channel(
        chat.id,
        chat.title,
        username
    )

    text = f"✅ Канал *{chat.title}* добавлен в каталог"
    if username:
        text += f"\n🔗 https://t.me/{username}"
    else:
        text += "\n⚠️ Канал без username (приватный)"

    await message.bot.send_message(
        chat.id,
        text,
        parse_mode="Markdown"
    )
