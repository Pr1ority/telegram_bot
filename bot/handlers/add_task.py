from aiogram import Router
from aiogram_dialog import Window, Dialog, DialogManager, StartMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.types import Message
import aiohttp

from config import API_URL, HEADERS

router = Router()


class AddTaskState(StatesGroup):
    title = State()
    category = State()


@router.message(Command('add_task'))
async def cmd_add_task(message:Message, dialog_manager: DialogManager):
    await dialog_manager.start(AddTaskState.title, mode=StartMode.NORMAL)


async def on_task_entered(
        message: Message, widget, manager: DialogManager, text: str):
    manager.dialog_data['title'] = text
    await manager.next()


async def on_category_entered(
        message: Message, widget, manager: DialogManager, text: str):
    manager.dialog_data['category'] = text

    payload = {
        'title': manager.dialog_data['title'],
        'category': manager.dialog_data['category']
    }

    headers = HEADERS.copy()
    headers['X-User-ID'] = str(message.from_user.id)

    async with aiohttp.ClientSession() as session:
        async with session.post(
            API_URL, json=payload, headers=headers
        ) as response:
            if response.status == 201:
                await message.answer('✅ Задача успешно добавлена!')
            else:
                await message.answer('❌ Не удалось добавить задачу')

        await manager.done()


add_task_dialog = Dialog(
    Window(
        Const('Введите вашу задачу'),
        TextInput(id='input_title', on_success=on_task_entered),
        state=AddTaskState.title,
    ),
    Window(
        Const('Укажите категорию задачи (например: Работа, Учёба, Хобби)'),
        TextInput(id='input_category', on_success=on_category_entered),
        state=AddTaskState.category,
    ),
)


dialog_router = Router()
dialog_router.include_routers(router, add_task_dialog)
