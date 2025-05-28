from aiogram.fsm.state import State,StatesGroup

class imput_data(StatesGroup):
    imput_user_agent = State()
    delit_admin = State()