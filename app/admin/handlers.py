import os
import json

from aiogram import Router, F
from aiogram.types import Message,FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.admin.keyboards import admin_button,remove_keybord
from app.admin.fms_state import imput_data


router = Router()


@router.message(Command("admin"))
async def admin_panel(message: Message):
    link_file = str(os.getcwd()) + "/media/admin.json"
    with open(link_file, "r", encoding="utf-8") as file:
        user_agents = json.load(file)
    user_name = "@"+ message.from_user.username
    if user_name in list(user_agents.values()):
        await message.answer("В админ панели администраторы могут:\n"
                             "1) получать файл с билетами\n"
                             "2) Подписаться на уведомление начала парсинга\n"
                             "3) Отписаться от уведомлений начала парсинга\n"
                             "4) Получить список админов\n"
                             "5) Добавить админа\n"
                             "6) Удалить админа\n"
                            ,reply_markup=admin_button)
    else:
        await message.answer("Вас нет в списке админов")


@router.message(F.text == "Добавить админа")
async def admin_panel(message: Message,state: FSMContext):
    await message.answer("Для добавление пользователя отправьте  его user_agent.\n пример '@юзер_агент'",reply_markup=remove_keybord)
    await state.set_state(imput_data.imput_user_agent)


@router.message(F.text == "Удалить админа")
async def admin_panel(message: Message,state: FSMContext):
    link_file = str(os.getcwd()) + "/media/admin.json"
    await message.answer("Введите номер админа.",reply_markup=remove_keybord)
    await state.set_state(imput_data.delit_admin)


@router.message(F.text == "Получить список админов")
async def admin_panel(message: Message):
    link_file = str(os.getcwd()) + "/media/admin.json"
    with open(link_file, "r", encoding="utf-8") as file:
        user_agents = json.load(file)
    json_pretty_string = json.dumps(user_agents, indent=4, ensure_ascii=False)
    print(json_pretty_string)
    await message.answer(json_pretty_string)


@router.message(F.text == "Подписаться на уведомление начала парсинга")
async def admin_panel(message: Message):
    link_file = str(os.getcwd()) + "/media/id_subscription.json"
    try:
        with open(link_file, "r", encoding="utf-8") as file:
            user_agents = json.load(file)
        max_id = max(map(int, user_agents.keys())) if user_agents else 0
        new_id = str(max_id + 1)

        user_agents[new_id] = message.from_user.id

        with open(link_file, "w", encoding="utf-8") as file:
            json.dump(user_agents, file, indent=4, ensure_ascii=False)
        await message.answer("Вы подписались", reply_markup=admin_button)

    except Exception:
        await message.answer("Произошла ошибка при подписке", reply_markup=admin_button)


@router.message(F.text == "Отписаться от уведомлений начала парсинга")
async def unsubscribe_from_notifications(message: Message):
    link_file = os.path.join(os.getcwd(), "media", "id_subscription.json")

    try:
        # Загрузка данных (с обработкой пустого файла)
        try:
            with open(link_file, "r", encoding="utf-8") as file:
                subscriptions = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            subscriptions = {}

        user_id = message.from_user.id  # Преобразуем ID в строку (ключи в JSON обычно строки)

        # Поиск и удаление подписки
        removed = False
        updated_subscriptions = {}

        for key, value in subscriptions.items():
            if value == user_id:  # Если это подписка текущего пользователя
                removed = True
            else:
                updated_subscriptions[key] = value  # Сохраняем другие подписки

        if removed:
            # Сохранение обновленных данных
            with open(link_file, "w", encoding="utf-8") as file:
                json.dump(updated_subscriptions, file, indent=4, ensure_ascii=False)
            await message.answer("Вы успешно отписались от уведомлений", reply_markup=admin_button)
        else:
            await message.answer("Вы не были подписаны на уведомления", reply_markup=admin_button)

    except Exception as e:
        print(f"Ошибка при отписке: {e}")
        await message.answer("Произошла ошибка при отписке", reply_markup=admin_button)



@router.message(F.text == "Получить файл")
async def admin_panel(message: Message):
    link_file = str(os.getcwd()) + "/media/ticket_list.txt"
    print(os.path.isfile(link_file))
    file = FSInputFile(link_file)
    await message.answer_document(document=file, caption="Вот ваш файл 📄")

@router.message(imput_data.imput_user_agent)
async def admin_panel(message: Message,state: FSMContext):
    link_file = str(os.getcwd()) + "/media/admin.json"
    try:
        with open(link_file, "r", encoding="utf-8") as file:
            user_agents = json.load(file)
        max_id = max(map(int, user_agents.keys())) if user_agents else 0
        new_id = str(max_id + 1)

        user_agents[new_id] = message.text

        with open(link_file, "w", encoding="utf-8") as file:
            json.dump(user_agents, file, indent=4, ensure_ascii=False)
        await message.answer("Админ успешно добавлен", reply_markup=admin_button)
        await state.clear()
    except Exception:
        await message.answer("Произошла ошибка при регистрации", reply_markup=admin_button)
        await state.clear()


@router.message(imput_data.delit_admin)
async def admin_panel(message: Message, state: FSMContext):
    link_file = str(os.getcwd()) + "/media/admin.json"
    try:
        with open(link_file, "r", encoding="utf-8") as file:
            user_agents = json.load(file)

        if message.text in user_agents:
            del user_agents[message.text]
        else:
            await message.answer("Произошла ошибка при удалении админа",reply_markup=admin_button)
            await state.clear()
            return

        with open(link_file, "w", encoding="utf-8") as file:
            json.dump(user_agents, file, indent=4, ensure_ascii=False)
        await message.answer("Админ успешно удален", reply_markup=admin_button)
        await state.clear()

    except Exception:
        await message.answer("Произошла ошибка при удалении админа", reply_markup=admin_button)
        await state.clear()




