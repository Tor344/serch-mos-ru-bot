import logging

logger = logging.getLogger("tor")
logger.setLevel(logging.DEBUG)

file_hendler = logging.FileHandler("media/loging/py_logging.log",mode="a")
file_hendler.setLevel(logging.WARNING)

console_hendler = logging.StreamHandler()
console_hendler.setLevel(logging.DEBUG)

console_formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

console_hendler.setFormatter(console_formatter)
file_hendler.setFormatter(file_formatter)

logger.addHandler(console_hendler)
logger.addHandler(file_hendler)