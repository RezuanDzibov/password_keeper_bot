from aiogram.dispatcher.filters.state import State, StatesGroup


class LoginCredentialsState(StatesGroup):
    site_name = State()
    account_login = State()
    account_password = State()


class StartState(StatesGroup):
    choice = State()


class AddRowState(StatesGroup):
    row_id = State()


class DeleteRowState(AddRowState):
    pass