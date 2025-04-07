import asyncio
import logging
import os
from aiohttp import web
from aiogram import Bot, Dispatcher
from config import TOKEN
from app.handler import router

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    await bot.delete_webhook()
    dp.include_router(router)
    await dp.start_polling(bot)

# Фейковый веб-сервер для Render (чтобы сервис не отключался)
async def fake_handler(request):
    return web.Response(text="I'm alive!")

async def start_fake_server():
    app = web.Application()
    app.router.add_get("/", fake_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.getenv("PORT", 8080)))
    await site.start()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start_fake_server())  # Запускаем фейковый сервер
    loop.run_until_complete(main())  # Запускаем бота
