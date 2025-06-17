from aiogram.fsm.state import State,StatesGroup

class imput_data(StatesGroup):
    input_user_agent = State()
    delit_admin = State()
    input_tate_ticket = State()
    input_time = State()