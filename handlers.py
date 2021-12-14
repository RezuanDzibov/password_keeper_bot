from aiogram import types
from aiogram.dispatcher import FSMContext, filters
from aiogram.types.message import ParseMode
from db import Database
import states
from bot import dp, bot, OWNER_ID
import aiogram.utils.markdown as md
from utils import return_formatted_rows


db = Database()


@dp.message_handler(commands='start', state=None)
async def start(message: types.Message):
    if message['from']['id'] != OWNER_ID:
        return await message.reply('Access denied.')
    await states.StartState.choice.set()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    markup.add('Show rows', 'Show row', 'Add row', 'Delete row')
    await message.reply('Choose option.', reply_markup=markup)


@dp.message_handler(filters.Text(contains='Show rows'), state=states.StartState.choice)
async def get_rows(message: types.Message, state: FSMContext):
    site_names = db.get_site_names()
    rows = await return_formatted_rows(site_names)
    if rows is not None:
        await message.answer(rows)
        await state.finish()
    else:
        await state.finish()
        await message.reply("You don't have any rows.")


@dp.message_handler(filters.Text(contains='Show row'), state=states.StartState)
async def get_row_id(message: types.Message):
    rows = await return_formatted_rows(db.get_site_names())
    if rows is not None:
        await message.answer(rows)
        await states.AddRowState.site_id.set()
        await message.reply('Input number of service.')
    else:
        await message.reply("You don't have any rows.")


@dp.message_handler(state=states.AddRowState.site_id)
async def get_row(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['site_id'] = message.text
        row = db.get_row(data['site_id'])
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Site name: ', row.site_name),
                md.text('Account login :', row.account_login),
                md.text('Account password:', row.account_password),
                sep='\n',
            ),
            parse_mode=ParseMode.MARKDOWN,
        )

        await state.finish()


@dp.message_handler(filters.Text(contains='Add row'), state=states.StartState)
async def add_row(message: types.Message):
    await states.LoginCredentialsState.site_name.set()
    await message.reply('Input site name.')


@dp.message_handler(state=states.LoginCredentialsState.site_name)
async def load_account_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['site_name'] = message.text
        await bot.send_message(message.chat.id, f"{data.get('site_name')}")
        await states.LoginCredentialsState.next()
        await message.reply('Input account login.')


@dp.message_handler(state=states.LoginCredentialsState.account_login)
async def load_account_login(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['account_login'] = message.text
        await bot.send_message(message.chat.id, f"{data.get('account_login')}")
        await states.LoginCredentialsState.next()
        await message.reply('Input account password.')


@dp.message_handler(state=states.LoginCredentialsState.account_password)
async def load_account_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['account_password'] = message.text
        db.insert_row(
            site_name=data['site_name'],
            account_login=data['account_login'],
            account_password=data['account_password']
        )
        await bot.send_message(
            message.chat.id,
            md.text(
                md.text('Site name: ', data.get('site_name')),
                md.text('Account login: ', data.get('account_login')),
                md.text('Account password: ', data.get('account_password')),
                sep='\n',
            ),
            parse_mode=ParseMode.MARKDOWN,
        )
    await state.finish()


@dp.message_handler(filters.Text(contains='Delete row'), state=states.StartState)
async def get_row_id_for_delete(message: types.Message):
    rows = await return_formatted_rows(db.get_site_names())
    if rows is not None:
        await message.answer(rows)
        await states.DeleteRowState.site_id.set()
        await message.reply('Input number of site.')
    else:
        await message.reply("You don't have any rows in your database.")


@dp.message_handler(state=states.DeleteRowState.site_id)
async def delete_row(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['site_id'] = message.text
        db.delete_row(data.get('site_id'))
        await bot.send_message(message.chat.id, f"Row with id {data.get('site_id')} has been deleted.")
        await state.finish()
