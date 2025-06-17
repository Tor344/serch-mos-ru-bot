from aiogram.types import KeyboardButton,ReplyKeyboardMarkup, ReplyKeyboardRemove

admin_button = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[
    [KeyboardButton(text="Получить файл")],
    [KeyboardButton(text="Подписаться на уведомление начала парсинга")],
    [KeyboardButton(text="Отписаться от уведомлений начала парсинга")],
    [KeyboardButton(text="Получить список админов")],
    [KeyboardButton(text="Добавить админа")],
    [KeyboardButton(text="Удалить админа")],
    [KeyboardButton(text="Получить сордированные билеты")],
    [KeyboardButton(text="Выбрать промежуток времени для регистрирование 120 билетов")]
])

remove_keybord = ReplyKeyboardRemove()