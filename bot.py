import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import start, add_channel, channels, post, common

async def main():
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(common.router)   # 🔥 ВАЖНО
    dp.include_router(add_channel.router)
    dp.include_router(channels.router)
    dp.include_router(post.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
