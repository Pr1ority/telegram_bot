from aiogram import Router
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Select
from aiogram_dialog.widgets.kbd import Back
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.types import Message
import aiohttp
from config import API_URL, HEADERS

router = Router()


class ViewByCategory(StatesGroup):
    choose_category = State()
    show_tasks = State()


@router.message(Command("tasks_by_category"))
async def cmd_tasks_by_category(
    message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(ViewByCategory.choose_category)


async def get_categories(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.event.from_user.id
    headers = HEADERS.copy()
    headers['X-User-ID'] = str(user_id)

    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, headers=headers) as response:
            if response.status != 200:
                return {"categories": []}
            tasks = await response.json()

    grouped = {}
    for task in tasks:
        cat = task["category_name"] or "Без категории"
        grouped.setdefault(cat, []).append(task)

    dialog_manager.dialog_data["grouped_tasks"] = grouped
    return {"categories": list(grouped.keys())}


async def get_tasks_for_category(dialog_manager: DialogManager, **kwargs):
    selected = dialog_manager.dialog_data.get("selected_category")
    grouped = dialog_manager.dialog_data.get("grouped_tasks", {})
    tasks = grouped.get(selected, [])

    if not tasks:
        return {"task_list": "В этой категории задач нет."}

    result = "\n".join(f"• {task['title']}" for task in tasks)
    return {"task_list": result}


async def on_category_selected(
        callback, widget, manager: DialogManager, item_id: str):
    manager.dialog_data["selected_category"] = item_id
    await manager.next()


view_by_category_dialog = Dialog(
    Window(
        Const("Выберите категорию:"),
        Select(
            Format("{item}"),
            id="category_select",
            item_id_getter=lambda x: x,
            items="categories",
            on_click=on_category_selected,
        ),
        state=ViewByCategory.choose_category,
        getter=get_categories,
    ),
    Window(
        Format("📂 Задачи в категории:\n\n{task_list}"),
        Back(Const("← Назад")),
        state=ViewByCategory.show_tasks,
        getter=get_tasks_for_category,
    ),
)

dialog_router = Router()
dialog_router.include_routers(router, view_by_category_dialog)
