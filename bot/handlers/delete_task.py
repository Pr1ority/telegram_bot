from aiogram import types, Router
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
import aiohttp

from config import API_URL, HEADERS

router = Router()


@router.message(Command('delete_task'))
async def delete_task_start(message: types.Message):
    """Выводит список задач для удаления"""

    headers = HEADERS.copy()
    headers['X-User-ID'] = str(message.from_user.id)

    async with aiohttp.ClientSession() as session:
        async with session.get(f'{API_URL}', headers=headers) as response:
            if response.status == 200:
                tasks = await response.json()
                if not tasks:
                    await message.answer('У вас нет задач для удаления')
                    return

                keyboard = InlineKeyboardMarkup(inline_keyboard=[])
                for task in tasks:
                    task_id = task['id']
                    task_title = task['title']
                    keyboard.inline_keyboard.append(
                        [
                            InlineKeyboardButton(
                                text=f'🗑 {task_title}',
                                callback_data=f'delete_{task_id}'
                            )
                        ]
                    )

                await message.answer(
                    'Выберите задачу для удаления:', reply_markup=keyboard
                )
            else:
                await message.answer('Ошибка при получении списка задач')


@router.callback_query(lambda c: c.data.startswith('delete_'))
async def confirm_delete_task(callback_query: types.CallbackQuery):
    """Подтверждение удаления"""
    task_id = callback_query.data.split('_')[1]

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    keyboard.inline_keyboard.append(
        [
            InlineKeyboardButton(
                text='✅ Удалить', callback_data=f'confirm_delete_{task_id}'
            )
        ]
    )
    keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text='❌ Отмена', callback_data='cancel_delete')]
    )

    await callback_query.message.edit_text(
        f'Вы уверены, что хотите удалить задачу?', reply_markup=keyboard
    )


@router.callback_query(lambda c: c.data.startswith('confirm_delete_'))
async def delete_task(callback_query: types.CallbackQuery):
    """Удаляет задачу после подтверждения"""
    task_id = callback_query.data.split('_')[2]
    user_id = callback_query.from_user.id

    headers = HEADERS.copy()
    headers['X-User-ID'] = str(user_id)

    async with aiohttp.ClientSession() as session:
        async with session.delete(
            f'{API_URL}{task_id}/', headers=headers
        ) as response:
            if response.status == 204:
                await callback_query.message.edit_text('✅ Задача удалена!')
            else:
                await callback_query.message.edit_text(
                    '❌ Ошибка при удалении задачи'
                )


@router.callback_query(lambda c: c.data == 'cancel_delete')
async def cancel_delete(callback_query: types.CallbackQuery):
    """Отмена удаления"""
    await callback_query.message.edit_text("Удаление отменено.")
