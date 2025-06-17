import logging
import os

# Создаем директорию, если её нет
log_dir = "media/loging"
os.makedirs(log_dir, exist_ok=True)  # exist_ok=True — не вызывает ошибку, если папка уже есть

logger = logging.getLogger("tor")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(os.path.join(log_dir, "py_logging.log"), mode="a")
file_handler.setLevel(logging.WARNING)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

console_formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

console_handler.setFormatter(console_formatter)
file_handler.setFormatter(file_formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
