import asyncio

from loader import bot, dp


from handlers import (
    start_router,
    question_router
)


async def run() -> None:
    dp.include_routers(start_router, question_router)

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot, )


if __name__ == '__main__':
    try:
        print('Bot started!')
        asyncio.run(run())
    except KeyboardInterrupt:
        print('Bot stopped!')