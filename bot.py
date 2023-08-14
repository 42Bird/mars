import os
import time
import asyncio
import logging
from dotenv import load_dotenv

from aiogram import types
from aiogram.bot import Bot
from aiogram.utils import executor
from aiogram.types import InputFile
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton


import parser_
from database import Database


load_dotenv()
PASSWORD = os.getenv('password')
FOLDER = r'/home/kali/ff/BOT2/заказ_2023.07.03_тгбот_парсУ/'

bot = Bot(token=os.getenv('token'))

storage = MemoryStorage()

dp = Dispatcher(bot=bot, storage=storage)

db = Database(db_file=os.getenv('db_file'))


"""

==================== /start and check password ===================="""

async def return_menu():
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton(text='Поиск по фамилии 👥', callback_data='surname'),
            InlineKeyboardButton(text='Поиск по фамилии и имени 👥',
                                 callback_data='lname_fname'),
            InlineKeyboardButton(text='Поиск по номеру телефона 📱',
                                 callback_data='number'),
            InlineKeyboardButton(text='Поиск по адресу жительства 🏠',
                                 callback_data='address'),
            InlineKeyboardButton(text='Поиск по подразделению 🛂',
                                 callback_data='structure'),
            InlineKeyboardButton(text='Поиск по дате рождения 🎂',
                                 callback_data='birth'),
            InlineKeyboardButton(text='Поиск по почте 📧', callback_data='mail'),
            InlineKeyboardButton(text='Поиск по ДРФО 🏢', callback_data='drfo'),
            InlineKeyboardButton(text='Поиск по паспорту 👤', callback_data='passport'),
            InlineKeyboardButton(text='Поиск по фото 🔍', callback_data='photo'),
            InlineKeyboardButton(text='Голосовой поиск 💬',
                                 callback_data='speech')
        )
        await msg.answer(text='Выберите критерий поиска', reply_markup=kb)
       
class UserPasswordWrong(StatesGroup):
    get_password = State()


@dp.message_handler(lambda msg: msg.chat.type == 'private', state='*', commands="start")
async def start(msg: types.Message, state: FSMContext):
    """
    Отвечает за /start. Если пользователя нет в БД, то добавляет его.
    Если пользователь до этого вводил верный пароль, то бот отправит клавиатуру,
    иначе попросит ввести пароль.
    """

    db.insert_in_tables(user_id=msg.from_user.id)
    await state.reset_state()

    photo = InputFile(path_or_bytesio=FOLDER + 'img/plakat14.jpg')
    caption = "Информационно-поисковая система 'Марс'"
    await msg.answer_photo(photo=photo, caption=caption)

    if db.user_password_is_correct(user_id=msg.from_user.id):
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton(text='Поиск по фамилии 👥', callback_data='surname'),
            InlineKeyboardButton(text='Поиск по фамилии и имени 👥',
                                 callback_data='lname_fname'),
            InlineKeyboardButton(text='Поиск по номеру телефона 📱',
                                 callback_data='number'),
            InlineKeyboardButton(text='Поиск по адресу жительства 🏠',
                                 callback_data='address'),
            InlineKeyboardButton(text='Поиск по подразделению 🛂',
                                 callback_data='structure'),
            InlineKeyboardButton(text='Поиск по дате рождения 🎂',
                                 callback_data='birth'),
            InlineKeyboardButton(text='Поиск по почте 📧', callback_data='mail'),
            InlineKeyboardButton(text='Поиск по ДРФО 🏢', callback_data='drfo'),
            InlineKeyboardButton(text='Поиск по паспорту 👤', callback_data='passport'),
            InlineKeyboardButton(text='Поиск по фото 🔍', callback_data='photo'),
            InlineKeyboardButton(text='Голосовой поиск 💬',
                                 callback_data='speech')
        )
        await msg.answer(text='Выберите критерий поиска', reply_markup=kb)
    else:
        await UserPasswordWrong.get_password.set()
        await msg.answer("Введите пароль!")


@dp.message_handler(lambda msg: msg.chat.type == 'private', state=UserPasswordWrong.get_password)
async def get_user_password(msg: types.Message, state: FSMContext):
    """
    Если пользователь ввел неверный пароль, то попадает сюда.
    Если введет верный, то бот отправит клавиатуру.
    """

    if msg.text == PASSWORD:
        db.change_password(user_id=msg.from_user.id, correct_password=1)
        await msg.answer('Добро пожаловать!')

        await state.reset_state()

        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton(text='Поиск по фамилии 👥', callback_data='surname'),
            InlineKeyboardButton(text='Поиск по фамилии и имени 👥',
                                 callback_data='lname_fname'),
            InlineKeyboardButton(text='Поиск по номеру телефона 📱',
                                 callback_data='number'),
            InlineKeyboardButton(text='Поиск по адресу жительства 🏠',
                                 callback_data='address'),
            InlineKeyboardButton(text='Поиск по подразделению 🛂',
                                 callback_data='structure'),
            InlineKeyboardButton(text='Поиск по дате рождения 🎂',
                                 callback_data='birth'),
            InlineKeyboardButton(text='Поиск по почте 📧', callback_data='mail'),
            InlineKeyboardButton(text='Поиск по ДРФО 🏢', callback_data='drfo'),
            InlineKeyboardButton(text='Поиск по паспорту 👤', callback_data='passport'),
            InlineKeyboardButton(text='Поиск по фото 🔍', callback_data='photo'),
            InlineKeyboardButton(text='Голосовой поиск 💬',
                                 callback_data='speech')
        )
        await msg.answer(text='Выберите критерий поиска', reply_markup=kb)

    else:
        await msg.answer('Неверный пароль!')

"""

====================  ===================="""


class ParserStates(StatesGroup):
    """
    Нужно для получения данных от пользователя.
    """
    get_surname = State()
    get_lname_fname = State()
    get_number = State()
    get_address = State()
    get_structure = State()
    get_birth = State()
    get_drfo = State()
    get_passport = State()
    get_photo = State()
    get_speech = State()


"""

==================== surname [по фамилии] ===================="""


@dp.callback_query_handler(lambda call: call.message.chat.type == 'private', text="surname")
async def surname_pars(call: types.CallbackQuery):
    await bot.send_message(chat_id=call.from_user.id, text='Введите фамилию. Пример ввода - Захарчук, Измайлов, Луговой')
    await ParserStates.get_surname.set()


@dp.message_handler(lambda msg: msg.chat.type == 'private', state=ParserStates.get_surname)
async def get_surname_for_pars(msg: types.Message, state: FSMContext):
    await bot.send_message(chat_id=msg.from_user.id, text=f'Начался поиск по фамилии {msg.text}')
    await state.reset_state()

    html = parser_.nemezida_surname(surname=msg.text)
    if html:
        filename = f'file_{time.time()}.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        # time.sleep(1)
        with open(filename, 'rb') as f:
            await msg.answer_document(f)
        # time.sleep(1)
        os.remove(filename)
        kb = InlineKeyboardMarkup(row_width=2)
        
        kb.add(
            InlineKeyboardButton(text='Поиск по фамилии 👥', callback_data='surname'),
            InlineKeyboardButton(text='Поиск по фамилии и имени 👥',
                                 callback_data='lname_fname'),
            InlineKeyboardButton(text='Поиск по номеру телефона 📱',
                                 callback_data='number'),
            InlineKeyboardButton(text='Поиск по адресу жительства 🏠',
                                 callback_data='address'),
            InlineKeyboardButton(text='Поиск по подразделению 🛂',
                                 callback_data='structure'),
            InlineKeyboardButton(text='Поиск по дате рождения 🎂',
                                 callback_data='birth'),
            InlineKeyboardButton(text='Поиск по почте 📧', callback_data='mail'),
            InlineKeyboardButton(text='Поиск по ДРФО 🏢', callback_data='drfo'),
            InlineKeyboardButton(text='Поиск по паспорту 👤', callback_data='passport'),
            InlineKeyboardButton(text='Поиск по фото 🔍', callback_data='photo'),
            InlineKeyboardButton(text='Голосовой поиск 💬',
                                 callback_data='speech')
        )
        await msg.answer(text='Выберите критерий поиска', reply_markup=kb)
    else:
        await bot.send_message(chat_id=msg.from_user.id, text=f'По {msg.text} ничего не найдено')
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton(text='Поиск по фамилии 👥', callback_data='surname'),
            InlineKeyboardButton(text='Поиск по фамилии и имени 👥',
                                 callback_data='lname_fname'),
            InlineKeyboardButton(text='Поиск по номеру телефона 📱',
                                 callback_data='number'),
            InlineKeyboardButton(text='Поиск по адресу жительства 🏠',
                                 callback_data='address'),
            InlineKeyboardButton(text='Поиск по подразделению 🛂',
                                 callback_data='structure'),
            InlineKeyboardButton(text='Поиск по дате рождения 🎂',
                                 callback_data='birth'),
            InlineKeyboardButton(text='Поиск по почте 📧', callback_data='mail'),
            InlineKeyboardButton(text='Поиск по ДРФО 🏢', callback_data='drfo'),
            InlineKeyboardButton(text='Поиск по паспорту 👤', callback_data='passport'),
            InlineKeyboardButton(text='Поиск по фото 🔍', callback_data='photo'),
            InlineKeyboardButton(text='Голосовой поиск 💬',
                                 callback_data='speech')
        )
        await msg.answer(text='Выберите критерий поиска', reply_markup=kb)

"""

==================== lname_fname [по имя и фамилии] ===================="""


@dp.callback_query_handler(lambda call: call.message.chat.type == 'private', text="lname_fname")
async def lname_fname_pars(call: types.CallbackQuery):
    await bot.send_message(chat_id=call.from_user.id, text='Введите имя и фамилию. Пример ввода - Алексей Захарчук, Сергей Измайлов, Борис Луговой')
    await ParserStates.get_lname_fname.set()


@dp.message_handler(lambda msg: msg.chat.type == 'private', state=ParserStates.get_lname_fname)
async def get_lname_fname_for_pars(msg: types.Message, state: FSMContext):
    await state.reset_state()
    await bot.send_message(chat_id=msg.from_user.id, text=f'Начался поиск по имя и фамилии {msg.text}')

    html = parser_.nemezida_lname_fname(lname_fname=msg.text)
    if html:
        filename = f'file_{time.time()}.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        time.sleep(1)
        with open(filename, 'rb') as f:
            await msg.answer_document(f)
        time.sleep(1)
        os.remove(filename)
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton(text='Поиск по фамилии 👥', callback_data='surname'),
            InlineKeyboardButton(text='Поиск по фамилии и имени 👥',
                                 callback_data='lname_fname'),
            InlineKeyboardButton(text='Поиск по номеру телефона 📱',
                                 callback_data='number'),
            InlineKeyboardButton(text='Поиск по адресу жительства 🏠',
                                 callback_data='address'),
            InlineKeyboardButton(text='Поиск по подразделению 🛂',
                                 callback_data='structure'),
            InlineKeyboardButton(text='Поиск по дате рождения 🎂',
                                 callback_data='birth'),
            InlineKeyboardButton(text='Поиск по почте 📧', callback_data='mail'),
            InlineKeyboardButton(text='Поиск по ДРФО 🏢', callback_data='drfo'),
            InlineKeyboardButton(text='Поиск по паспорту 👤', callback_data='passport'),
            InlineKeyboardButton(text='Поиск по фото 🔍', callback_data='photo'),
            InlineKeyboardButton(text='Голосовой поиск 💬',
                                 callback_data='speech')
        )
        await msg.answer(text='Выберите критерий поиска', reply_markup=kb)
    else:
        await bot.send_message(chat_id=msg.from_user.id, text=f'По {msg.text} ничего не найдено')
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton(text='Поиск по фамилии 👥', callback_data='surname'),
            InlineKeyboardButton(text='Поиск по фамилии и имени 👥',
                                 callback_data='lname_fname'),
            InlineKeyboardButton(text='Поиск по номеру телефона 📱',
                                 callback_data='number'),
            InlineKeyboardButton(text='Поиск по адресу жительства 🏠',
                                 callback_data='address'),
            InlineKeyboardButton(text='Поиск по подразделению 🛂',
                                 callback_data='structure'),
            InlineKeyboardButton(text='Поиск по дате рождения 🎂',
                                 callback_data='birth'),
            InlineKeyboardButton(text='Поиск по почте 📧', callback_data='mail'),
            InlineKeyboardButton(text='Поиск по ДРФО 🏢', callback_data='drfo'),
            InlineKeyboardButton(text='Поиск по паспорту 👤', callback_data='passport'),
            InlineKeyboardButton(text='Поиск по фото 🔍', callback_data='photo'),
            InlineKeyboardButton(text='Голосовой поиск 💬',
                                 callback_data='speech')
        )
        await msg.answer(text='Выберите критерий поиска', reply_markup=kb)

"""

==================== number [по номеру] ===================="""


@dp.callback_query_handler(lambda call: call.message.chat.type == 'private', text="number")
async def number_pars(call: types.CallbackQuery):
    await bot.send_message(chat_id=call.from_user.id, text='Введите номер телефона. Пример ввода - 380962391128, 79256789456')
    await ParserStates.get_number.set()


@dp.message_handler(lambda msg: msg.chat.type == 'private', state=ParserStates.get_number)
async def get_number_for_pars(msg: types.Message, state: FSMContext):

    await bot.send_message(chat_id=msg.from_user.id, text=f'Начался поиск по номеру {msg.text}')
    await state.reset_state()

    html = parser_.nemezida_other(req_text=msg.text)
    if html:
        filename = f'file_{time.time()}.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        time.sleep(1)
        with open(filename, 'rb') as f:
            await msg.answer_document(f)
        time.sleep(1)
        os.remove(filename)
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton(text='Поиск по фамилии 👥', callback_data='surname'),
            InlineKeyboardButton(text='Поиск по фамилии и имени 👥',
                                 callback_data='lname_fname'),
            InlineKeyboardButton(text='Поиск по номеру телефона 📱',
                                 callback_data='number'),
            InlineKeyboardButton(text='Поиск по адресу жительства 🏠',
                                 callback_data='address'),
            InlineKeyboardButton(text='Поиск по подразделению 🛂',
                                 callback_data='structure'),
            InlineKeyboardButton(text='Поиск по дате рождения 🎂',
                                 callback_data='birth'),
            InlineKeyboardButton(text='Поиск по почте 📧', callback_data='mail'),
            InlineKeyboardButton(text='Поиск по ДРФО 🏢', callback_data='drfo'),
            InlineKeyboardButton(text='Поиск по паспорту 👤', callback_data='passport'),
            InlineKeyboardButton(text='Поиск по фото 🔍', callback_data='photo'),
            InlineKeyboardButton(text='Голосовой поиск 💬',
                                 callback_data='speech')
        )
        await msg.answer(text='Выберите критерий поиска', reply_markup=kb)
    else:
        await bot.send_message(chat_id=msg.from_user.id, text=f'По {msg.text} ничего не найдено')
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton(text='Поиск по фамилии 👥', callback_data='surname'),
            InlineKeyboardButton(text='Поиск по фамилии и имени 👥',
                                 callback_data='lname_fname'),
            InlineKeyboardButton(text='Поиск по номеру телефона 📱',
                                 callback_data='number'),
            InlineKeyboardButton(text='Поиск по адресу жительства 🏠',
                                 callback_data='address'),
            InlineKeyboardButton(text='Поиск по подразделению 🛂',
                                 callback_data='structure'),
            InlineKeyboardButton(text='Поиск по дате рождения 🎂',
                                 callback_data='birth'),
            InlineKeyboardButton(text='Поиск по почте 📧', callback_data='mail'),
            InlineKeyboardButton(text='Поиск по ДРФО 🏢', callback_data='drfo'),
            InlineKeyboardButton(text='Поиск по паспорту 👤', callback_data='passport'),
            InlineKeyboardButton(text='Поиск по фото 🔍', callback_data='photo'),
            InlineKeyboardButton(text='Голосовой поиск 💬',
                                 callback_data='speech')
        )
        await msg.answer(text='Выберите критерий поиска', reply_markup=kb)

"""

==================== address [по адресу] ===================="""


@dp.callback_query_handler(lambda call: call.message.chat.type == 'private', text="address")
async def address_pars(call: types.CallbackQuery):
    await bot.send_message(chat_id=call.from_user.id, text='Введите адрес. Пример ввода - Украина, Киевская область, город Киев, проспект Победы, д. 55/2')
    await ParserStates.get_address.set()


@dp.message_handler(lambda msg: msg.chat.type == 'private', state=ParserStates.get_address)
async def get_address_for_pars(msg: types.Message, state: FSMContext):

    await bot.send_message(chat_id=msg.from_user.id, text=f'Начался поиск по адресу {msg.text}')
    await state.reset_state()

    html = parser_.nemezida_other(req_text=msg.text)
    if html:
        filename = f'file_{time.time()}.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        time.sleep(1)
        with open(filename, 'rb') as f:
            await msg.answer_document(f)
        time.sleep(1)
        os.remove(filename)
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton(text='Поиск по фамилии 👥', callback_data='surname'),
            InlineKeyboardButton(text='Поиск по фамилии и имени 👥',
                                 callback_data='lname_fname'),
            InlineKeyboardButton(text='Поиск по номеру телефона 📱',
                                 callback_data='number'),
            InlineKeyboardButton(text='Поиск по адресу жительства 🏠',
                                 callback_data='address'),
            InlineKeyboardButton(text='Поиск по подразделению 🛂',
                                 callback_data='structure'),
            InlineKeyboardButton(text='Поиск по дате рождения 🎂',
                                 callback_data='birth'),
            InlineKeyboardButton(text='Поиск по почте 📧', callback_data='mail'),
            InlineKeyboardButton(text='Поиск по ДРФО 🏢', callback_data='drfo'),
            InlineKeyboardButton(text='Поиск по паспорту 👤', callback_data='passport'),
            InlineKeyboardButton(text='Поиск по фото 🔍', callback_data='photo'),
            InlineKeyboardButton(text='Голосовой поиск 💬',
                                 callback_data='speech')
        )
        await msg.answer(text='Выберите критерий поиска', reply_markup=kb)
    else:
        await bot.send_message(chat_id=msg.from_user.id, text=f'По {msg.text} ничего не найдено')
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton(text='Поиск по фамилии 👥', callback_data='surname'),
            InlineKeyboardButton(text='Поиск по фамилии и имени 👥',
                                 callback_data='lname_fname'),
            InlineKeyboardButton(text='Поиск по номеру телефона 📱',
                                 callback_data='number'),
            InlineKeyboardButton(text='Поиск по адресу жительства 🏠',
                                 callback_data='address'),
            InlineKeyboardButton(text='Поиск по подразделению 🛂',
                                 callback_data='structure'),
            InlineKeyboardButton(text='Поиск по дате рождения 🎂',
                                 callback_data='birth'),
            InlineKeyboardButton(text='Поиск по почте 📧', callback_data='mail'),
            InlineKeyboardButton(text='Поиск по ДРФО 🏢', callback_data='drfo'),
            InlineKeyboardButton(text='Поиск по паспорту 👤', callback_data='passport'),
            InlineKeyboardButton(text='Поиск по фото 🔍', callback_data='photo'),
            InlineKeyboardButton(text='Голосовой поиск 💬',
                                 callback_data='speech')
        )
        await msg.answer(text='Выберите критерий поиска', reply_markup=kb)
"""

==================== structure [по подразделению] ===================="""


@dp.callback_query_handler(lambda call: call.message.chat.type == 'private', text="structure")
async def structure_pars(call: types.CallbackQuery):
    await bot.send_message(chat_id=call.from_user.id, text='Введите подразделение. Пример ввода - Полк Азов, СБУ')
    await ParserStates.get_structure.set()


@dp.message_handler(lambda msg: msg.chat.type == 'private', state=ParserStates.get_structure)
async def get_structure_for_pars(msg: types.Message, state: FSMContext):

    await bot.send_message(chat_id=msg.from_user.id, text=f'Начался поиск по подразделению {msg.text}')
    await state.reset_state()

    html = parser_.nemezida_other(req_text=msg.text)
    if html:
        filename = f'file_{time.time()}.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        time.sleep(1)
        with open(filename, 'rb') as f:
            await msg.answer_document(f)
        time.sleep(1)
        os.remove(filename)
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton(text='Поиск по фамилии 👥', callback_data='surname'),
            InlineKeyboardButton(text='Поиск по фамилии и имени 👥',
                                 callback_data='lname_fname'),
            InlineKeyboardButton(text='Поиск по номеру телефона 📱',
                                 callback_data='number'),
            InlineKeyboardButton(text='Поиск по адресу жительства 🏠',
                                 callback_data='address'),
            InlineKeyboardButton(text='Поиск по подразделению 🛂',
                                 callback_data='structure'),
            InlineKeyboardButton(text='Поиск по дате рождения 🎂',
                                 callback_data='birth'),
            InlineKeyboardButton(text='Поиск по почте 📧', callback_data='mail'),
            InlineKeyboardButton(text='Поиск по ДРФО 🏢', callback_data='drfo'),
            InlineKeyboardButton(text='Поиск по паспорту 👤', callback_data='passport'),
            InlineKeyboardButton(text='Поиск по фото 🔍', callback_data='photo'),
            InlineKeyboardButton(text='Голосовой поиск 💬',
                                 callback_data='speech')
        )
        await msg.answer(text='Выберите критерий поиска', reply_markup=kb)
    else:
        await bot.send_message(chat_id=msg.from_user.id, text=f'По {msg.text} ничего не найдено')
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton(text='Поиск по фамилии 👥', callback_data='surname'),
            InlineKeyboardButton(text='Поиск по фамилии и имени 👥',
                                 callback_data='lname_fname'),
            InlineKeyboardButton(text='Поиск по номеру телефона 📱',
                                 callback_data='number'),
            InlineKeyboardButton(text='Поиск по адресу жительства 🏠',
                                 callback_data='address'),
            InlineKeyboardButton(text='Поиск по подразделению 🛂',
                                 callback_data='structure'),
            InlineKeyboardButton(text='Поиск по дате рождения 🎂',
                                 callback_data='birth'),
            InlineKeyboardButton(text='Поиск по почте 📧', callback_data='mail'),
            InlineKeyboardButton(text='Поиск по ДРФО 🏢', callback_data='drfo'),
            InlineKeyboardButton(text='Поиск по паспорту 👤', callback_data='passport'),
            InlineKeyboardButton(text='Поиск по фото 🔍', callback_data='photo'),
            InlineKeyboardButton(text='Голосовой поиск 💬',
                                 callback_data='speech')
        )
        await msg.answer(text='Выберите критерий поиска', reply_markup=kb)

"""

==================== birth [по дню рождению] ===================="""


@dp.callback_query_handler(lambda call: call.message.chat.type == 'private', text="birth")
async def birth_pars(call: types.CallbackQuery):
    await bot.send_message(chat_id=call.from_user.id, text='Введите день рождения. Пример ввода - 14.06.1990')
    await ParserStates.get_birth.set()


@dp.message_handler(lambda msg: msg.chat.type == 'private', state=ParserStates.get_birth)
async def get_birth_for_pars(msg: types.Message, state: FSMContext):

    await bot.send_message(chat_id=msg.from_user.id, text=f'Начался поиск по дню рождению {msg.text}')
    await state.reset_state()

    html = parser_.nemezida_other(req_text=msg.text)
    if html:
        filename = f'file_{time.time()}.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        time.sleep(1)
        with open(filename, 'rb') as f:
            await msg.answer_document(f)
        time.sleep(1)
        os.remove(filename)
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton(text='Поиск по фамилии 👥', callback_data='surname'),
            InlineKeyboardButton(text='Поиск по фамилии и имени 👥',
                                 callback_data='lname_fname'),
            InlineKeyboardButton(text='Поиск по номеру телефона 📱',
                                 callback_data='number'),
            InlineKeyboardButton(text='Поиск по адресу жительства 🏠',
                                 callback_data='address'),
            InlineKeyboardButton(text='Поиск по подразделению 🛂',
                                 callback_data='structure'),
            InlineKeyboardButton(text='Поиск по дате рождения 🎂',
                                 callback_data='birth'),
            InlineKeyboardButton(text='Поиск по почте 📧', callback_data='mail'),
            InlineKeyboardButton(text='Поиск по ДРФО 🏢', callback_data='drfo'),
            InlineKeyboardButton(text='Поиск по паспорту 👤', callback_data='passport'),
            InlineKeyboardButton(text='Поиск по фото 🔍', callback_data='photo'),
            InlineKeyboardButton(text='Голосовой поиск 💬',
                                 callback_data='speech')
        )
        await msg.answer(text='Выберите критерий поиска', reply_markup=kb)
    else:
        await bot.send_message(chat_id=msg.from_user.id, text=f'По {msg.text} ничего не найдено')
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton(text='Поиск по фамилии 👥', callback_data='surname'),
            InlineKeyboardButton(text='Поиск по фамилии и имени 👥',
                                 callback_data='lname_fname'),
            InlineKeyboardButton(text='Поиск по номеру телефона 📱',
                                 callback_data='number'),
            InlineKeyboardButton(text='Поиск по адресу жительства 🏠',
                                 callback_data='address'),
            InlineKeyboardButton(text='Поиск по подразделению 🛂',
                                 callback_data='structure'),
            InlineKeyboardButton(text='Поиск по дате рождения 🎂',
                                 callback_data='birth'),
            InlineKeyboardButton(text='Поиск по почте 📧', callback_data='mail'),
            InlineKeyboardButton(text='Поиск по ДРФО 🏢', callback_data='drfo'),
            InlineKeyboardButton(text='Поиск по паспорту 👤', callback_data='passport'),
            InlineKeyboardButton(text='Поиск по фото 🔍', callback_data='photo'),
            InlineKeyboardButton(text='Голосовой поиск 💬',
                                 callback_data='speech')
        )
        await msg.answer(text='Выберите критерий поиска', reply_markup=kb)
"""

==================== drfo [по ДРФО] ===================="""


@dp.callback_query_handler(lambda call: call.message.chat.type == 'private', text="drfo")
async def drfo_pars(call: types.CallbackQuery):
    await bot.send_message(chat_id=call.from_user.id, text='Введите ДРФО. Пример ввода - 3303701415, 2808517692')
    await ParserStates.get_drfo.set()


@dp.message_handler(lambda msg: msg.chat.type == 'private', state=ParserStates.get_drfo)
async def get_drfo_for_pars(msg: types.Message, state: FSMContext):

    await bot.send_message(chat_id=msg.from_user.id, text=f'Начался поиск по ДРФО {msg.text}')
    await state.reset_state()

    html = parser_.nemezida_other(req_text=msg.text)
    if html:
        filename = f'file_{time.time()}.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        time.sleep(1)
        with open(filename, 'rb') as f:
            await msg.answer_document(f)
        time.sleep(1)
        os.remove(filename)
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton(text='Поиск по фамилии 👥', callback_data='surname'),
            InlineKeyboardButton(text='Поиск по фамилии и имени 👥',
                                 callback_data='lname_fname'),
            InlineKeyboardButton(text='Поиск по номеру телефона 📱',
                                 callback_data='number'),
            InlineKeyboardButton(text='Поиск по адресу жительства 🏠',
                                 callback_data='address'),
            InlineKeyboardButton(text='Поиск по подразделению 🛂',
                                 callback_data='structure'),
            InlineKeyboardButton(text='Поиск по дате рождения 🎂',
                                 callback_data='birth'),
            InlineKeyboardButton(text='Поиск по почте 📧', callback_data='mail'),
            InlineKeyboardButton(text='Поиск по ДРФО 🏢', callback_data='drfo'),
            InlineKeyboardButton(text='Поиск по паспорту 👤', callback_data='passport'),
            InlineKeyboardButton(text='Поиск по фото 🔍', callback_data='photo'),
            InlineKeyboardButton(text='Голосовой поиск 💬',
                                 callback_data='speech')
        )
        await msg.answer(text='Выберите критерий поиска', reply_markup=kb)
    else:
        await bot.send_message(chat_id=msg.from_user.id, text=f'По {msg.text} ничего не найдено')
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton(text='Поиск по фамилии 👥', callback_data='surname'),
            InlineKeyboardButton(text='Поиск по фамилии и имени 👥',
                                 callback_data='lname_fname'),
            InlineKeyboardButton(text='Поиск по номеру телефона 📱',
                                 callback_data='number'),
            InlineKeyboardButton(text='Поиск по адресу жительства 🏠',
                                 callback_data='address'),
            InlineKeyboardButton(text='Поиск по подразделению 🛂',
                                 callback_data='structure'),
            InlineKeyboardButton(text='Поиск по дате рождения 🎂',
                                 callback_data='birth'),
            InlineKeyboardButton(text='Поиск по почте 📧', callback_data='mail'),
            InlineKeyboardButton(text='Поиск по ДРФО 🏢', callback_data='drfo'),
            InlineKeyboardButton(text='Поиск по паспорту 👤', callback_data='passport'),
            InlineKeyboardButton(text='Поиск по фото 🔍', callback_data='photo'),
            InlineKeyboardButton(text='Голосовой поиск 💬',
                                 callback_data='speech')
        )
        await msg.answer(text='Выберите критерий поиска', reply_markup=kb)
"""

==================== passport [по паспорту] ===================="""


@dp.callback_query_handler(lambda call: call.message.chat.type == 'private', text="passport")
async def passport_pars(call: types.CallbackQuery):
    await bot.send_message(chat_id=call.from_user.id, text='Введите паспорт. Пример ввода - ВМ243442, НМ269938')
    await ParserStates.get_passport.set()


@dp.message_handler(lambda msg: msg.chat.type == 'private', state=ParserStates.get_passport)
async def get_passport_for_pars(msg: types.Message, state: FSMContext):
    await bot.send_message(chat_id=msg.from_user.id, text=f'Начался поиск по паспорту {msg.text}')
    await state.reset_state()

    html = parser_.nemezida_other(req_text=msg.text)
    if html:
        filename = f'file_{time.time()}.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        time.sleep(1)
        with open(filename, 'rb') as f:
            await msg.answer_document(f)
        time.sleep(1)
        os.remove(filename)
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton(text='Поиск по фамилии 👥', callback_data='surname'),
            InlineKeyboardButton(text='Поиск по фамилии и имени 👥',
                                 callback_data='lname_fname'),
            InlineKeyboardButton(text='Поиск по номеру телефона 📱',
                                 callback_data='number'),
            InlineKeyboardButton(text='Поиск по адресу жительства 🏠',
                                 callback_data='address'),
            InlineKeyboardButton(text='Поиск по подразделению 🛂',
                                 callback_data='structure'),
            InlineKeyboardButton(text='Поиск по дате рождения 🎂',
                                 callback_data='birth'),
            InlineKeyboardButton(text='Поиск по почте 📧', callback_data='mail'),
            InlineKeyboardButton(text='Поиск по ДРФО 🏢', callback_data='drfo'),
            InlineKeyboardButton(text='Поиск по паспорту 👤', callback_data='passport'),
            InlineKeyboardButton(text='Поиск по фото 🔍', callback_data='photo'),
            InlineKeyboardButton(text='Голосовой поиск 💬',
                                 callback_data='speech')
        )
        await msg.answer(text='Выберите критерий поиска', reply_markup=kb)
    else:
        await bot.send_message(chat_id=msg.from_user.id, text=f'По {msg.text} ничего не найдено')
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton(text='Поиск по фамилии 👥', callback_data='surname'),
            InlineKeyboardButton(text='Поиск по фамилии и имени 👥',
                                 callback_data='lname_fname'),
            InlineKeyboardButton(text='Поиск по номеру телефона 📱',
                                 callback_data='number'),
            InlineKeyboardButton(text='Поиск по адресу жительства 🏠',
                                 callback_data='address'),
            InlineKeyboardButton(text='Поиск по подразделению 🛂',
                                 callback_data='structure'),
            InlineKeyboardButton(text='Поиск по дате рождения 🎂',
                                 callback_data='birth'),
            InlineKeyboardButton(text='Поиск по почте 📧', callback_data='mail'),
            InlineKeyboardButton(text='Поиск по ДРФО 🏢', callback_data='drfo'),
            InlineKeyboardButton(text='Поиск по паспорту 👤', callback_data='passport'),
            InlineKeyboardButton(text='Поиск по фото 🔍', callback_data='photo'),
            InlineKeyboardButton(text='Голосовой поиск 💬',
                                 callback_data='speech')
        )
        await msg.answer(text='Выберите критерий поиска', reply_markup=kb)
"""

==================== photo [по фото] ===================="""


@dp.callback_query_handler(lambda call: call.message.chat.type == 'private', text="photo")
async def photo_pars(call: types.CallbackQuery):
    await bot.send_message(chat_id=call.from_user.id, text='Отправьте фото военнослужащего ВСУ')
    await ParserStates.get_photo.set()


# @dp.message_handler(lambda msg: msg.chat.type == 'private', state=ParserStates.get_photo, content_types=['photo', 'text'])
# async def get_photo_for_pars(msg: types.Message, state: FSMContext):
#     if msg.photo:
#         await bot.send_message(chat_id=msg.from_user.id, text=f'Начался поиск по фото')
#     else:
#         await msg.answer('Надо отправить фото!')
#     await state.reset_state()

@dp.message_handler(lambda msg: msg.chat.type == 'private', state=ParserStates.get_photo, content_types=['photo', 'text'])
async def get_photo_for_pars(message: types.Message, state: FSMContext):
    await state.reset_state()

    try:

        # # Получаем информацию о фото
        #     file_info = await bot.get_file(message.photo[-1].file_id)
        #     file_path = file_info.file_path
        # # Скачиваем фото
        #     downloaded_file = await bot.download_file(file_path)
        # # Сохраняем фото в файле
        #     with open("find.jpg", 'wb') as photo_file:
        #         photo_file.write(downloaded_file)

        await message.photo[-1].download('find.jpg')

        await bot.send_message(message.chat.id, "Идет поиск по фото... ⏳")

        import os
        import dlib
        import numpy as np
        from skimage import io
        from scipy.spatial import distance
        import shutil
        import threading

        def get_file_list(dirpath):
            file_list = []
            for root, dirs, files in os.walk(dirpath):
                for name in files:
                    fullname = os.path.join(root, name)
                    if any(ext in fullname.lower() for ext in ['.jpg', '.jpeg']):
                        file_list.append(fullname)
            return file_list

        def get_face_descriptors(filename, detector, sp, face_rec):
            face_descriptors = []
            img = io.imread(filename)
            detected_faces = detector(img, 1)

            for d in detected_faces:
                shape = sp(img, d)
                try:
                    face_descriptor = face_rec.compute_face_descriptor(
                        img, shape)
                    if face_descriptor is not None:
                        face_descriptors.append(face_descriptor)
                except Exception as ex:
                    pass

            return face_descriptors

        if __name__ == '__main__':
            dirpath_0 = 'photos/group_0/'
            dirpath_1 = 'photos/group_1/'
            dirpath_2 = 'photos/group_2/'
            dirpath_3 = 'photos/group_3/'
            dirpath_4 = 'photos/group_4/'
            dirpath_5 = 'photos/group_5/'
            dirpath_6 = 'photos/group_6/'
            dirpath_7 = 'photos/group_7/'
            dirpath_8 = 'photos/group_8/'
            dirpath_9 = 'photos/group_9/'
            dirpath_10 = 'photos/group_10/'
            dirpath_11 = 'photos/group_11/'
            dirpath_12 = 'photos/group_12/'
            dirpath_13 = 'photos/group_13/'
            dirpath_14 = 'photos/group_14/'
            dirpath_15 = 'photos/group_15/'

            resultpath = ''
            obrazec = 'find.jpg'
            vsego = 0

            detector = dlib.get_frontal_face_detector()
            sp = dlib.shape_predictor(
                'shape_predictor_68_face_landmarks.dat')  # FIXME
            face_rec = dlib.face_recognition_model_v1(
                'dlib_face_recognition_resnet_model_v1.dat')  # FIXME

            min_distance = 0.561

            f1 = get_face_descriptors(obrazec, detector, sp, face_rec)[0]
            files_0 = get_file_list(dirpath_0)
            files_1 = get_file_list(dirpath_1)
            files_2 = get_file_list(dirpath_2)
            files_3 = get_file_list(dirpath_3)
            files_4 = get_file_list(dirpath_4)
            files_5 = get_file_list(dirpath_5)
            files_6 = get_file_list(dirpath_6)
            files_7 = get_file_list(dirpath_7)
            files_8 = get_file_list(dirpath_8)
            files_9 = get_file_list(dirpath_9)
            files_10 = get_file_list(dirpath_10)
            files_11 = get_file_list(dirpath_11)
            files_12 = get_file_list(dirpath_12)
            files_13 = get_file_list(dirpath_13)
            files_14 = get_file_list(dirpath_14)
            files_15 = get_file_list(dirpath_15)

            vsego = str(len(files_0 + files_1 + files_2 + files_3 + files_4 + files_5 + files_6 + files_7 +
                        files_8 + files_9 + files_10 + files_11 + files_12 + files_13 + files_14 + files_15))
            print('Готовится к анализу: ' + vsego + ' фотографий')

            # lst_filename = []
            async def f(filename):
                await bot.send_photo(message.chat.id, photo=open(f'{filename}.jpg', 'rb'), caption=f"Имя - {filename[:-4]}")

            # async def compare(files):

            def compare(files):
                flag = 0
                for idx, f in enumerate(files):
                    flag += 1
                    try:
                        find_faces = get_face_descriptors(
                            f, detector, sp, face_rec)
                        for f2 in find_faces:
                            euc_distance = distance.euclidean(f1, f2)
                            if euc_distance < min_distance:
                                print(
                                    f'Евклидово расстояние: {euc_distance:.3f} - Найдено лицо: {f}')
                                filename = os.path.basename(f)
                                shutil.copyfile(f, os.path.join(
                                    resultpath, f'{filename}.jpg'))

                                import telebot
                                bot_telebot = telebot.TeleBot('6243379302:AAE0bZN3v32-V58wrge8c5ziALrVdX_Ue1c')
                                bot_telebot.send_photo(message.chat.id, photo = open(f'{filename}.jpg', 'rb'))
                                bot_telebot.send_message(message.chat.id, text = f"Имя - {filename[4:]}")
                                # lst_filename.append(filename)
                                asyncio.run(f(filename))

                    except:
                        continue

            import multiprocessing
            files_list = [files_0, files_1, files_2, files_3, files_4,
                          files_5, files_6, files_7, files_8, files_9, files_10, files_11, files_12, files_13, files_14, files_15]

            processes = []
            for files in files_list:
                process = multiprocessing.Process(
                    target=compare, args=(files,))
                processes.append(process)
                process.start()

            for process in processes:
                process.join()
                kb = InlineKeyboardMarkup(row_width=2)
                kb.add(
            InlineKeyboardButton(text='Поиск по фамилии 👥', callback_data='surname'),
            InlineKeyboardButton(text='Поиск по фамилии и имени 👥',
                                 callback_data='lname_fname'),
            InlineKeyboardButton(text='Поиск по номеру телефона 📱',
                                 callback_data='number'),
            InlineKeyboardButton(text='Поиск по адресу жительства 🏠',
                                 callback_data='address'),
            InlineKeyboardButton(text='Поиск по подразделению 🛂',
                                 callback_data='structure'),
            InlineKeyboardButton(text='Поиск по дате рождения 🎂',
                                 callback_data='birth'),
            InlineKeyboardButton(text='Поиск по почте 📧', callback_data='mail'),
            InlineKeyboardButton(text='Поиск по ДРФО 🏢', callback_data='drfo'),
            InlineKeyboardButton(text='Поиск по паспорту 👤', callback_data='passport'),
            InlineKeyboardButton(text='Поиск по фото 🔍', callback_data='photo'),
            InlineKeyboardButton(text='Голосовой поиск 💬',
                                 callback_data='speech')
        )
        await msg.answer(text='Выберите критерий поиска', reply_markup=kb)

            # for filename in lst_filename:
            #     await bot.send_photo(message.chat.id, photo=open(f'{filename}.jpg', 'rb'), caption=f"Имя - {filename[:-4]}")

    except Exception as e:
        print(e)
        await bot.send_message(message.chat.id, "Произошла ошибка при сохранении фото.")
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton(text='Поиск по фамилии 👥', callback_data='surname'),
            InlineKeyboardButton(text='Поиск по фамилии и имени 👥',
                                 callback_data='lname_fname'),
            InlineKeyboardButton(text='Поиск по номеру телефона 📱',
                                 callback_data='number'),
            InlineKeyboardButton(text='Поиск по адресу жительства 🏠',
                                 callback_data='address'),
            InlineKeyboardButton(text='Поиск по подразделению 🛂',
                                 callback_data='structure'),
            InlineKeyboardButton(text='Поиск по дате рождения 🎂',
                                 callback_data='birth'),
            InlineKeyboardButton(text='Поиск по почте 📧', callback_data='mail'),
            InlineKeyboardButton(text='Поиск по ДРФО 🏢', callback_data='drfo'),
            InlineKeyboardButton(text='Поиск по паспорту 👤', callback_data='passport'),
            InlineKeyboardButton(text='Поиск по фото 🔍', callback_data='photo'),
            InlineKeyboardButton(text='Голосовой поиск 💬',
                                 callback_data='speech')
        )
        await msg.answer(text='Выберите критерий поиска', reply_markup=kb)


"""

==================== speech [по голосу] ===================="""


@dp.callback_query_handler(lambda call: call.message.chat.type == 'private', text="speech")
async def speech_pars(call: types.CallbackQuery):
    await bot.send_message(chat_id=call.from_user.id, text='Отправьте голосовое сообщение. Пример ввода - 380962391128, 79256789456')
    await ParserStates.get_speech.set()


@dp.message_handler(lambda msg: msg.chat.type == 'private', state=ParserStates.get_speech, content_types=['voice'])
async def get_speech_for_pars(msg: types.Message, state: FSMContext = ParserStates.get_speech):
    await state.reset_state()

    await bot.send_message(chat_id=msg.from_user.id, text=f'Начался поиск по голосу {msg.text}')

    # TODO


"""

==================== if __name__ == "__main__": ===================="""


if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    db.create_tables()
    print("===== bot online =====")
    executor.start_polling(dispatcher=dp, skip_updates=True)
