import time
import uuid

from aiogram import Bot

import bot
import keyboards as k
from db import *

bot = Bot(token=TOKEN)


async def generate_file_url():
    return str(uuid.uuid4())


async def add_user(user_id, username):
    data_about_user = await select_db("*", "users", f"user_id = {user_id}")
    if data_about_user == []:
        await insert_db("users", ("user_id", "username", "time_reg"), (user_id, username, int(time.time())))
    else:
        if data_about_user[0][2] != username:
            await update_db("users", "username", f"'{username}'", f"user_id = {user_id}")


async def send_file(user_id, file_url, bms):
    data_about_file = await select_db("*", "files", f"file_url = '{file_url}'")
    file_id = data_about_file[0][3]
    type_ = data_about_file[0][2]
    description = data_about_file[0][5]
    caption = f"<i>{bms.name}:</i> <code>{data_about_file[0][7]}</code>"  # \n\n<i>Описание: </i><code>{description}</code>"
    if description != "":
        caption += f"\n\n<i>{bms.discription}: </i><code>{description}</code>"
    # bot.file["caption"] = caption
    if int(user_id) == int(data_about_file[0][1]):
        all_about_file = await select_db("amount", "files_click", f"file_url = '{file_url}'")
        uniq_click = len(all_about_file)
        all_click = 0
        for code in all_about_file:
            all_click += int(code[0])

        all_data_files = bms.all_data_files.split("-----")
        public_link = all_data_files[0]
        all_download = all_data_files[1]
        uniq_download = all_data_files[2]

        text = f"\n\n{public_link} t.me/{bot_username}?start={data_about_file[0][4]}\n\n<i>{all_download} </i><code>{all_click}</code>\n<i>{uniq_download}</i> <code>{uniq_click}</code>"
        caption += text
        if type_ == "audio":
            await bot.send_audio(user_id, file_id, caption=caption, reply_markup=await k.edit_file(bms),
                                 parse_mode="html")
        elif type_ == "document":
            await bot.send_document(user_id, file_id, caption=caption, reply_markup=await k.edit_file(),
                                    parse_mode="html")
        elif type_ == "photo":
            await bot.send_photo(user_id, file_id, caption=caption, reply_markup=await k.edit_file(bms),
                                 parse_mode="html")
        elif type_ == "video":
            await bot.send_video(user_id, file_id, caption=caption, reply_markup=await k.edit_file(bms),
                                 parse_mode="html")
    else:
        if type_ == "audio":
            await bot.send_audio(user_id, file_id, caption=caption, parse_mode="html")
        elif type_ == "document":
            await bot.send_document(user_id, file_id, caption=caption, parse_mode="html")
        elif type_ == "photo":
            await bot.send_photo(user_id, file_id, caption=caption, parse_mode="html")
        elif type_ == "video":
            await bot.send_video(user_id, file_id, caption=caption, parse_mode="html")

    data_about_click = await select_db('*', "files_click", f"user_id = {user_id} AND file_url = '{file_url}'")
    if data_about_file[0][1] != user_id:
        if data_about_click == []:
            await insert_db("files_click", ("user_id", "file_url", "amount", "first_time", "last_time"),
                            (user_id, file_url, 1, int(time.time()), int(time.time())))
        else:
            # data_about_click = await select_db("*", "files_click", f"user_id = {user_id} AND file_url = '{file_url}'")
            amount = int(data_about_click[0][3])
            await update_db("files_click", 'amount', amount + 1,
                            f"user_id = {user_id} AND file_url = '{file_url}'")
            await update_db("files_click", 'last_time', int(time.time()),
                            f"user_id = {user_id} AND file_url = '{file_url}'")


async def edit_message(chat_id, message_id, text, reply_markup):
    await bot.edit_message_text(text, chat_id=chat_id, message_id=message_id, parse_mode="html",
                                disable_web_page_preview=True)
    await bot.edit_message_reply_markup(chat_id, message_id=message_id, reply_markup=await reply_markup)


async def edit_user_balance(user_id: int, edit_summ: str):
    user_balance = await select_db("balance", "users", f"user_id = {user_id}")
    user_balance = float(user_balance[0][0])
    await update_db("users", "balance", round(user_balance + float(edit_summ), 1), f"user_id = {user_id}")


async def add_files(message, bms):
    global type_, file_url
    if message.content_type == "audio":
        file_id = message.audio.file_id
        file_url = await generate_file_url()
        type_ = "audio"
        file_name = message.audio.file_name
        user = await select_db("*", "users", f"user_id = {message.from_user.id}")
        if user != []:
            await insert_db("files", ("user_id", "type", "file_id", "file_url", "description", "time_add", "file_name"),
                            (message.from_user.id, type_, file_id, file_url, "", int(time.time()), file_name))
        else:
            await add_user(message.from_user.id, message.from_user.username)
            await insert_db("files", ("user_id", "type", "file_id", "file_url", "description", "time_add", "file_name"),
                            (message.from_user.id, type_, file_id, file_url, "", int(time.time()), file_name))
        # caption = f"<b>Успешно добавлено!</b>\n\nИмя файла: {file_name}\n\nОписание: - \n\nСсылка:\nhttps://t.me/{bot_username}?start={file_url}"
    elif message.content_type == "document":
        file_id = message.document.file_id
        file_name = message.document.file_name
        file_url = await generate_file_url()
        type_ = "document"
        user = await select_db("*", "users", f"user_id = {message.from_user.id}")
        if user != []:
            await insert_db("files", ("user_id", "type", "file_id", "file_url", "description", "time_add", "file_name"),
                            (message.from_user.id, type_, file_id, file_url, "", int(time.time()), file_name))
        else:
            await add_user(message.from_user.id, message.from_user.username)
            await insert_db("files", ("user_id", "type", "file_id", "file_url", "description", "time_add", "file_name"),
                            (message.from_user.id, type_, file_id, file_url, "", int(time.time()), file_name))
        # caption = f"<b>Успешно добавлено!</b>\n\nИмя файла: {file_name}\n\nОписание: - \n\nСсылка:\nhttps://t.me/{bot_username}?start={file_url}"
    elif message.content_type == "photo":
        file_id = message.photo[0].file_id
        file_url = await generate_file_url()
        amount_photo = await select_db("*", "files", f"type = 'photo' AND user_id = {message.from_user.id}")
        file_name = "photo " + str(len(amount_photo) + 1)
        type_ = "photo"
        user = await select_db("*", "users", f"user_id = {message.from_user.id}")
        if user != []:
            await insert_db("files", ("user_id", "type", "file_id", "file_url", "description", "time_add", "file_name"),
                            (message.from_user.id, type_, file_id, file_url, "", int(time.time()), file_name))
        else:
            await add_user(message.from_user.id, message.from_user.username)
            await insert_db("files", ("user_id", "type", "file_id", "file_url", "description", "time_add", "file_name"),
                            (message.from_user.id, type_, file_id, file_url, "", int(time.time()), file_name))
        # caption = f"<b>Успешно добавлено!</b>\n\nИмя файла: {file_name}\n\nОписание: - \n\nСсылка:\nhttps://t.me/{bot_username}?start={file_url}"
    elif message.content_type == "video":
        file_id = message.video.file_id
        file_name = message.video.file_name
        file_url = await generate_file_url()
        type_ = "video"
        user = await select_db("*", "users", f"user_id = {message.from_user.id}")
        if user != []:
            await insert_db("files", ("user_id", "type", "file_id", "file_url", "description", "time_add", "file_name"),
                            (message.from_user.id, type_, file_id, file_url, "", int(time.time()), file_name))
        else:
            await add_user(message.from_user.id, message.from_user.username)
            await insert_db("files", ("user_id", "type", "file_id", "file_url", "description", "time_add", "file_name"),
                            (message.from_user.id, type_, file_id, file_url, "", int(time.time()), file_name))
        # caption = f"<b>Успешно добавлено!</b>\n\nИмя файла: {file_name}\n\nОписание: - \n\nСсылка:\nhttps://t.me/{bot_username}?start={file_url}"

    else:
        i_can_not = bms.i_can_not.split("-----")
        unsupported_format = i_can_not[0]
        support = i_can_not[1]
        video = i_can_not[2]
        photos = i_can_not[3]
        audio = i_can_not[4]
        documents = i_can_not[5]
        caption = f"{unsupported_format}! ({support}: <i>{video}</i>, <i>{photos}</i>, <i>{audio}</i>, <i>{documents}</i>)"
        file_url = ""
    all_data_files = bms.all_data_files.split("-----")
    public_link = all_data_files[0]
    caption = f"<b>{bms.success}!</b>\n\n{bms.name}: {file_name}\n\n{bms.discription}: - \n\n{public_link}\nhttps://t.me/{bot_username}?start={file_url}"
    return [caption, file_url]
