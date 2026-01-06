from aiogram import Router, F
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from database import can_post, update_post_time, get_channel
from filters import bad_words_check
from handlers.common import (
    send_clean,
    back_kb,
    user_channel,
    user_post
)

router = Router()


@router.callback_query(F.data.startswith("select_"))
async def select_channel(callback: CallbackQuery):
    channel_id = int(callback.data.split("_")[1])
    user_channel[callback.from_user.id] = channel_id

    await send_clean(
        callback.message,
        "✍️ Пришлите рекламный пост одним сообщением",
        reply_markup=back_kb()
    )
    await callback.answer()


@router.message()
async def receive_post(message: Message):
    user_id = message.from_user.id
    if user_id not in user_channel:
        return

    text = message.text or ""

    if bad_words_check(text):
        await send_clean(message, "❌ Реклама запрещена правилами", back_kb())
        return

    if not can_post(user_id):
        await send_clean(message, "⏳ Можно публиковать 1 пост в 24 часа", back_kb())
        return

    channel_id = user_channel[user_id]
    channel = get_channel(channel_id)

    if not channel:
        await send_clean(message, "❌ Канал не найден", back_kb())
        user_channel.pop(user_id, None)
        return

    _, title, username = channel
    user_post[user_id] = text

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔔 Открыть канал",
                    url=f"https://t.me/{username}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Я подписался",
                    callback_data="check_subscribe"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="back"
                )
            ]
        ]
    )

    await send_clean(
        message,
        f"❗ Подпишитесь на канал «{title}», затем нажмите кнопку ниже",
        reply_markup=kb
    )


@router.callback_query(F.data == "check_subscribe")
async def check_subscribe(callback: CallbackQuery):
    user_id = callback.from_user.id

    if user_id not in user_channel or user_id not in user_post:
        await callback.answer("❌ Данные устарели", show_alert=True)
        return

    channel_id = user_channel[user_id]
    bot = callback.bot

    try:
        member = await bot.get_chat_member(channel_id, user_id)

        if member.status in ("member", "administrator", "creator"):
            await bot.send_message(channel_id, user_post[user_id])
            update_post_time(user_id)

            user_channel.pop(user_id, None)
            user_post.pop(user_id, None)

            await callback.message.edit_text("✅ Пост успешно опубликован")
        else:
            await callback.answer("❌ Вы не подписались на канал", show_alert=True)

    except Exception:
        await callback.answer("❌ Подпишитесь на канал и попробуйте снова", show_alert=True)
