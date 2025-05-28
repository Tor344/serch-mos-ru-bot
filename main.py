import os
import json
from datetime import datetime

from aiogram import Bot, Dispatcher
import config.settings as set
from app.start.handlers import router as start_router
from app.user.handlers import router as user_router
from app.admin.handlers import router as admin_router
from app.sergh_mos_ru.handlers import router as sergh_mos_ru_router
from app.sergh_mos_ru.grant import monitor_mos_ru


async def main():
    bot = Bot(token=set.API_TOKEN)
    dp = Dispatcher()
    dp.include_router(user_router)
    dp.include_router(admin_router)
    dp.include_router(start_router)
    dp.include_router(sergh_mos_ru_router)
    asyncio.create_task(monitor_mos_ru_loop(bot))
    await dp.start_polling(bot)

import asyncio

async def send_notifications(bot: Bot):
    """Функция для отправки уведомлений всем пользователям из базы данных"""
    link_file = str(os.getcwd()) + "/media/id_subscription.json"

    with open(link_file, "r", encoding="utf-8") as file:
        user_agents = json.load(file)

    for key, user in user_agents.items():
        try:
            user = int(user)
            await bot.send_message(
                chat_id=user,  # Предполагается, что в БД есть поле user_id
                text="🔔 Появились новые билеты на mos.ru! Регистрация началась"
            )
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {user.user_id}: {e}")

async def monitor_mos_ru_loop(bot):
    while True:
        now = datetime.now()
        if datetime.weekday(now) == 3:
            print("Запуск мониторинга...")
            try:
                flag = await asyncio.to_thread(monitor_mos_ru)
                if flag == True:
                    await send_notifications(bot)
            except Exception as e:
                print(f"Ошибка мониторинга: {e}")
        await asyncio.sleep(10)  # каждые 30 секунд

if __name__ == "__main__":
    asyncio.run(main())