import aiogram
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import keyboards as k
from db import *
import time
import random
import other_func as of
from datetime import datetime

from config import *
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

CONTENT_TYPES = ["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact"]

file = {"url": "", "dis": "", "name": "", "caption": ""}

action = "pass"




@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    if "/start" in message.text:
        await of.add_user(message.from_user.id, message.from_user.username)
        if len(message.text.split()) > 1:
            file_url = message.text.split()[1]
            data_about_file = await select_db("*", "files", f"file_url = '{file_url}'")
            if data_about_file != []:
                await of.send_file(message.from_user.id, file_url)
                file["url"] = file_url
            else:
                await bot.send_message(message.from_user.id, "Найдите достоверную ссылку",
                                       reply_markup=await k.only_support())
        else:
            await bot.send_message(message.from_user.id,
                                   "Этот бот предназначен для получения файлов. Поэтому сначала найди ссылку ну или отправь мне файл",
                                   reply_markup=await k.only_support())
    else:
        await bot.send_message(message.from_user.id,
                               "Этот бот предназначен для получения файлов. Поэтому сначала найди ссылку",
                               reply_markup=await k.only_support())

@dp.message_handler(commands=['me'])
async def process_start_command(message: types.Message):
    files_data = await select_db("*", "files", f"user_id = {message.from_user.id}")
    caption = "Это все твои файлы\n\n"
    for i in files_data:
        text = f"<a href='https://t.me/{bot_username}?start={i[4]}'>{i[7]}</a>\n\n"
        caption += text
    if caption == "Это все твои файлы\n\n":
        caption = "У тебя нет загруженых файлов"
    await bot.send_message(message.from_user.id, caption, parse_mode="html", disable_web_page_preview=True)

@dp.message_handler(commands=['help'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Этот бот предназначен для получения файлов.\nМожешь мне отправить файл, а я дам ссылку\n\nЕсли что пиши @csb_support_bot", parse_mode="html")


@dp.callback_query_handler()
async def callback_inline(call):
    try:
        global action
        global file
        if call.data == "support":
            caption = "Если возникли проблемы с установкой, запуском приложения, то обратись к администратору канала в котором ты взял приложение\n\nПроблемы или ошибки в боте: @CSB_support_bot"
            await bot.send_message(call.message.chat.id, caption)
        elif call.data == "my_files":
            file_url = file["url"]
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            files_data = await select_db("*", "files", f"user_id = {call.message.chat.id}")
            caption = "Это все твои файлы\n\n"
            for i in files_data:
                text = f"<a href='https://t.me/{bot_username}?start={i[4]}'>{i[7]}</a>\n\n"
                caption += text
            await bot.send_message(call.message.chat.id, caption, parse_mode="html", disable_web_page_preview=True)
        elif call.data == "add_description":
            action = "add_description"
            caption = "Отправь мне описание"
            await bot.send_message(call.message.chat.id, caption)
        elif call.data == "edit_name":
            action = "edit_name"
            caption = "Отправь мне новое имя файла"
            await bot.send_message(call.message.chat.id, caption)
        elif call.data == "reload":
            file_url = file["url"]
            data_about_file = await select_db("*", "files", f"file_url = '{file_url}'")
            description = data_about_file[0][5]
            caption = f"<i>Название:</i> <code>{data_about_file[0][7]}</code>"#\n\n<i>Описание: </i><code>{description}</code>"
            if description != "":
                caption += f"\n\n<i>Описание: </i><code>{description}</code>"
            all_about_file = await select_db("amount", "files_click", f"file_url = '{file_url}'")
            uniq_click = len(all_about_file)
            all_click = 0
            for code in all_about_file:
                all_click += int(code[0])
            caption += f"\n\nПубличная ссылка: t.me/{bot_username}?start={file_url}\n\n<i>Все скачивания: </i><code>{all_click}</code>\n<i>Уникальные скачивания:</i> <code>{uniq_click}</code>"
            try:
                await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=caption, parse_mode="html", reply_markup=await k.edit_file())
            except:
                await call.answer("Изменений нет")
        elif call.data == "delete":
            file_url = file["url"]
            await delete_db("files_click", f"file_url = '{file_url}'")
            await delete_db("files", f"file_url = '{file_url}'")
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            files_data = await select_db("*", "files", f"user_id = {call.message.chat.id}")
            caption = "Это все твои файлы\n\n"
            for i in files_data:
                text = f"<a href='https://t.me/{bot_username}?start={i[4]}'>{i[7]}</a>\n\n"
                caption += text
            await bot.send_message(call.message.chat.id, caption, parse_mode="html")
    except IndexError:
        await bot.send_message(call.message.chat.id, "Меня только что перезапустили, или возникла непредвиденая ситуация лучше об этом напиши @csb_support_bot")


@dp.message_handler(content_types=CONTENT_TYPES)
async def what_message(message: types.Message):
    global file
    global action
    if message.content_type == "text":
        if action == "add_description":
            file["dis"] = message.text
            url = file["url"]
            dis = file["dis"]
            await update_db("files", "description", f"'{dis}'", f"file_url = '{url}'")
            await of.send_file(message.from_user.id, file["url"])
            action = "pass"
            file = {"url": file["url"], "dis": "", "name": "", "caption": ""}

        elif action == "edit_name":
            file["name"] = message.text
            url = file["url"]
            name = file["name"]
            await update_db("files", "file_name", f"'{name}'", f"file_url = '{url}'")
            await of.send_file(message.from_user.id, file["url"])
            action = "pass"
            file = {"url": file["url"], "dis": "", "name": "", "caption": ""}
        else:
            await bot.send_message(message.from_user.id, "Прости, что?\nНапиши лучше /start")
    else:
        msg = await of.add_files(message)
        file["url"] = msg[1]
        caption = msg[0]
        await bot.send_message(message.from_user.id, caption, parse_mode="html",
                               reply_markup=await k.add_description())

if __name__ == '__main__':
    executor.start_polling(dp)
