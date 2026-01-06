from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database import get_channels
from handlers.common import send_clean, back_kb

router = Router()

@router.callback_query(F.data == "channels")
async def show_channels(callback: CallbackQuery):
    channels = get_channels()

    if not channels:
        await send_clean(callback.message, "❌ Каналов пока нет", back_kb())
        return

    keyboard = []

    for channel_id, title, username in channels:
        keyboard.append([
            InlineKeyboardButton(
                text=f"📣 {title}",
                callback_data=f"select_{channel_id}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data="back"
        )
    ])

    await send_clean(
        callback.message,
        "📢 *Выберите канал:*",
        InlineKeyboardMarkup(inline_keyboard=keyboard),
        parse_mode="Markdown"
    )
