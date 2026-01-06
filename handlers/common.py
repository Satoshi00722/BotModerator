from aiogram import Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

router = Router()

# ОБЩИЕ ХРАНИЛИЩА
user_channel = {}
user_post = {}
last_bot_message = {}

def back_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="back"
                )
            ]
        ]
    )

async def send_clean(message, text, reply_markup=None, parse_mode=None):
    user_id = message.from_user.id

    if user_id in last_bot_message:
        try:
            await message.bot.delete_message(
                message.chat.id,
                last_bot_message[user_id]
            )
        except:
            pass

    msg = await message.answer(
        text,
        reply_markup=reply_markup,
        parse_mode=parse_mode
    )
    last_bot_message[user_id] = msg.message_id


@router.callback_query(F.data == "back")
async def back_handler(callback: CallbackQuery):
    user_id = callback.from_user.id

    user_channel.pop(user_id, None)
    user_post.pop(user_id, None)

    from handlers.channels import show_channels
    await show_channels(callback)

    await callback.answer()
