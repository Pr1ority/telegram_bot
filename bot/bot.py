import asyncio
import logging
import os

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.filters import Command
from aiogram_dialog import setup_dialogs

from config import API_URL, HEADERS
from handlers import delete_task, add_task, edit_task, task_by_category

TOKEN = os.getenv('TOKEN', 'TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)

storage = MemoryStorage()

dp = Dispatcher(storage=storage)
dp.include_router(delete_task.router)
dp.include_router(add_task.dialog_router)
dp.include_routers(edit_task.dialog_router)
dp.include_routers(
    task_by_category.dialog_router
)
setup_dialogs(dp)


@dp.message(Command('start'))
async def start_handler(message: Message):
    await message.answer('Привет! Я бот для управления задачами')


@dp.message(Command('tasks'))
async def send_tasks(message: Message):

    headers = HEADERS.copy()
    headers['X-User-ID'] = str(message.from_user.id)

    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, headers=headers) as response:
            if response.status == 200:
                tasks = await response.json()
                if tasks:
                    text = '\n'.join(
                        [
                            f'📌 {task["title"]}\n'
                            f'🗂 Категория: {task["category_name"]}\n'
                            f'📅 {task["created_at"]}\n'

                            for task in tasks
                        ]
                    )
                else:
                    text = 'У вас пока нет задач'
            else:
                text = 'Ошибка при получении задач 😞'
    await message.answer(text)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
