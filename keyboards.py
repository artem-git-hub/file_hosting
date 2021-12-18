from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def only_support():
    only_support = InlineKeyboardMarkup(row_width=1)
    support = InlineKeyboardButton("Поддержка", callback_data="support")
    only_support.add(support)
    return only_support


async def add_description():
    add_description = InlineKeyboardMarkup(row_width=2)
    add = InlineKeyboardButton("Добавить описание", callback_data="add_description")
    name = InlineKeyboardButton("Изменить имя файла", callback_data="edit_name")
    add_description.add(add, name)
    return add_description



async def edit_file():
    edit_file = InlineKeyboardMarkup(row_width=1)
    add = InlineKeyboardButton("Изменить описание", callback_data="add_description")
    name = InlineKeyboardButton("Изменить имя файла", callback_data="edit_name")
    my_files = InlineKeyboardButton("Мои файлы", callback_data="my_files")
    reload = InlineKeyboardButton("Обновить", callback_data="reload")
    delete = InlineKeyboardButton("Удалить", callback_data="delete")
    edit_file.row(add)
    edit_file.row(name)
    edit_file.row(my_files)
    edit_file.row(delete, reload)
    return edit_file

async def pass_but():
    edit_file = InlineKeyboardMarkup(row_width=1)
    add = InlineKeyboardButton("", callback_data="pass")
    edit_file.row(add)
    return edit_file
