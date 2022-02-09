from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def only_support(bms):
    only_support = InlineKeyboardMarkup(row_width=1)
    support = InlineKeyboardButton(bms.support_msg, callback_data="support")
    only_support.add(support)
    return only_support


async def add_description(bms):
    add_description = InlineKeyboardMarkup(row_width=2)
    add = InlineKeyboardButton(bms.edit_description, callback_data="add_description")
    name = InlineKeyboardButton(bms.edit_name, callback_data="edit_name")
    add_description.add(add, name)
    return add_description


async def edit_file(bms):
    edit_file = InlineKeyboardMarkup(row_width=1)
    add = InlineKeyboardButton(bms.edit_description, callback_data="add_description")
    name = InlineKeyboardButton(bms.edit_name, callback_data="edit_name")
    my_files = InlineKeyboardButton(bms.my_files, callback_data="my_files")
    reload = InlineKeyboardButton(bms.reload, callback_data="reload")
    delete = InlineKeyboardButton(bms.delete, callback_data="delete")
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


async def i_agree(bms):
    i_agree = InlineKeyboardMarkup(row_width=1)
    yes = InlineKeyboardButton(f"🟩        {bms.i_agree}        🟩", callback_data="i_agree")
    no = InlineKeyboardButton(f"🟥  {bms.disagree}  🟥", callback_data="do_not_agree")
    i_agree.row(no)
    i_agree.row(yes)
    return i_agree


async def but_for_add(text, link, with_confirm=False, count="Не указан"):
    but_for_add = InlineKeyboardMarkup(row_width=1)
    for i in range(0, len(text)):
        button = InlineKeyboardButton(text=text[i], url=link[i])
        but_for_add.row(button)

    delete_msg = InlineKeyboardButton("Удалить", callback_data="delete_msg")
    but_for_add.add(delete_msg)
    if with_confirm:
        confirm = InlineKeyboardButton(" - Подтверждаю - ", callback_data="confirm")
        but_for_add.add(confirm)
        count = InlineKeyboardButton(f"Количество - - ({count})", callback_data="count_this_is_no")
        but_for_add.add(count)
    return but_for_add
