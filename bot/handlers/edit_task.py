from aiogram import Router
from aiogram_dialog import Window, Dialog, DialogManager, StartMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Select
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.types import Message
import aiohttp

from config import API_URL, HEADERS

router = Router()


class EditTaskState(StatesGroup):
    choose_task = State()
    new_title = State()
    new_category = State()


@router.message(Command('edit_task'))
async def cmd_edit_task(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        EditTaskState.choose_task, mode=StartMode.NORMAL
    )


async def get_tasks(dialog_manager: DialogManager, **kwargs):
    headers = HEADERS.copy()
    headers['X-User-ID'] = str(dialog_manager.event.from_user.id)
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, headers=headers) as response:
            if response.status == 200:
                tasks = await response.json()
                return {"tasks": tasks}
            return {"tasks": []}


async def on_task_selected(
        callback, widget, manager: DialogManager, task_id: str):
    manager.dialog_data['task_id'] = task_id
    await manager.next()


async def on_title_entered(
        message: Message, widget, manager: DialogManager, text: str):
    manager.dialog_data['new_title'] = text
    await manager.next()


async def on_category_entered(
        message: Message, widget, manager: DialogManager, text: str):
    manager.dialog_data['new_category'] = text

    task_id = manager.dialog_data['task_id']
    payload = {
        'title': manager.dialog_data['new_title'],
        'category_name': manager.dialog_data['new_category']
    }

    headers = HEADERS.copy()
    headers['X-User-ID'] = str(message.from_user.id)

    async with aiohttp.ClientSession() as session:
        async with session.patch(
            f"{API_URL}{task_id}/", json=payload, headers=headers
        ) as response:
            if response.status == 200:
                await message.answer("✅ Задача успешно отредактирована!")
            elif response.status == 404:
                await message.answer("❌ Задача не найдена")
            else:
                await message.answer("❌ Не удалось отредактировать задачу")

    await manager.done()


edit_task_dialog = Dialog(
    Window(
        Const("Выберите задачу для редактирования"),
        Select(
            Format("{item[title]} (Категория: {item[category_name]})"),
            id="task_selector",
            item_id_getter=lambda x: str(x["id"]),
            items="tasks",
            on_click=on_task_selected,
        ),
        getter=get_tasks,
        state=EditTaskState.choose_task,
    ),
    Window(
        Const("Введите новое название задачи"),
        TextInput(id="input_title", on_success=on_title_entered),
        state=EditTaskState.new_title,
    ),
    Window(
        Const("Введите новую категорию задачи"),
        TextInput(id="input_category", on_success=on_category_entered),
        state=EditTaskState.new_category,
    ),
)

dialog_router = Router()
dialog_router.include_routers(router, edit_task_dialog)
