import time
from random import randint

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import keyboards
import keyboards as k
import other_func as of
from db import *
from messages_bot import Bmsg

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

CONTENT_TYPES = ["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact"]

file = {"url": "", "dis": "", "name": "", "caption": ""}

action = "pass"
advertising = "pass"
advertising_data = {"photo": None, "text": "", "entities": [], "button": {"text": [], "link": []}, "count": 0}


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    bms = Bmsg(message.from_user.language_code)
    if "/start" in message.text:
        await of.add_user(message.from_user.id, message.from_user.username)
        if len(message.text.split()) > 1:
            file_url = message.text.split()[1]
            data_about_file = await select_db("*", "files", f"file_url = '{file_url}'")
            if data_about_file != []:
                await of.send_file(message.from_user.id, file_url, bms)
                file["url"] = file_url
            else:
                await bot.send_message(message.from_user.id, bms.give_link,
                                       reply_markup=await k.only_support(bms))
        else:
            await bot.send_message(message.from_user.id,
                                   bms.about_me,
                                   reply_markup=await k.only_support(bms))
    else:
        await bot.send_message(message.from_user.id,
                               bms.about_me,
                               reply_markup=await k.only_support(bms))


@dp.message_handler(commands=['advertising'])
async def process_start_command(message: types.Message):
    # print(message.from_user.username)
    global advertising
    if message.from_user.username == "cha_artem":
        await bot.send_message(chat_id=message.from_user.id, text=f"Send me photo or no send 'none'")
        advertising = "photo"
    else:
        await bot.send_message(message.from_user.id, "Прости, что?\nНапиши лучше /start")


@dp.message_handler(commands=['me'])
async def process_start_command(message: types.Message):
    bms = Bmsg(message.from_user.language_code)
    files_data = await select_db("*", "files", f"user_id = {message.from_user.id}")
    caption = f"{bms.all_files}\n\n"
    for i in files_data:
        text = f"<a href='https://t.me/{bot_username}?start={i[4]}'>{i[7]}</a>\n\n"
        caption += text
    if caption == f"{bms.all_files}\n\n":
        caption = bms.not_files
    await bot.send_message(message.from_user.id, caption, parse_mode="html", disable_web_page_preview=True)


@dp.message_handler(commands=['help'])
async def process_start_command(message: types.Message):
    bms = Bmsg(message.from_user.language_code)
    await bot.send_message(message.from_user.id,
                           bms.about_me,
                           parse_mode="html")


@dp.callback_query_handler()
async def callback_inline(call):
    bms = Bmsg(call["from"].language_code)
    try:
        global action
        global file

        if call.data == "confirm" and call.message.chat.username == "cha_artem":
            # print(call.message.chat.username)
            users_id = await select_db("user_id", "users")
            for_send_message = []
            if advertising_data["count"] == "all":
                for_send_message = users_id
            elif type(advertising_data["count"]) is int:
                count = int(advertising_data["count"])
                max_id = len(users_id) - count
                start_id = randint(0, max_id - 2)
                # print(start_id, max_id)
                for i in range(start_id, start_id + count):
                    for_send_message.append(users_id[i])
                # print(len(for_send_message))

            for i in for_send_message:
                try:
                    if advertising_data['photo'] is not None:
                        await bot.send_photo(chat_id=i[0], caption=advertising_data['text'],
                                             reply_markup=await keyboards.but_for_add(
                                                 advertising_data["button"]["text"],
                                                 advertising_data["button"]["link"]),
                                             caption_entities=advertising_data["entities"],
                                             photo=advertising_data['photo'], )
                    else:
                        await bot.send_message(chat_id=i[0], text=advertising_data['text'],
                                               reply_markup=await keyboards.but_for_add(
                                                   advertising_data["button"]["text"],
                                                   advertising_data["button"]["link"]), disable_web_page_preview=True,
                                               entities=advertising_data["entities"])
                    time.sleep(0.5)
                except Exception as e:
                    print(e)
            global advertising
            advertising = "pass"
            advertising_data["photo"] = None
            advertising_data["text"] = ""
            advertising_data["entities"]: []
            advertising_data["button"] = {"text": [], "link": []}
            advertising_data["count"] = 0

        elif call.data == "delete_msg":
            await bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == "support":
            caption = bms.support
            await bot.send_message(call.message.chat.id, caption)
        elif call.data == "my_files":
            file_url = file["url"]
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            files_data = await select_db("*", "files", f"user_id = {call.message.chat.id}")
            caption = f"{bms.all_files}\n\n"
            for i in files_data:
                text = f"<a href='https://t.me/{bot_username}?start={i[4]}'>{i[7]}</a>\n\n"
                caption += text
            await bot.send_message(call.message.chat.id, caption, parse_mode="html", disable_web_page_preview=True)
        elif call.data == "add_description":
            action = "add_description"
            caption = bms.send_discripion
            await bot.send_message(call.message.chat.id, caption)
        elif call.data == "edit_name":
            action = "edit_name"
            caption = bms.send_name_file
            await bot.send_message(call.message.chat.id, caption)
        elif call.data == "reload":
            file_url = file["url"]
            data_about_file = await select_db("*", "files", f"file_url = '{file_url}'")
            description = data_about_file[0][5]
            caption = f"<i>{bms.name}:</i> <code>{data_about_file[0][7]}</code>"
            if description != "":
                caption += f"\n\n<i>{bms.discription}: </i><code>{description}</code>"
            all_about_file = await select_db("amount", "files_click", f"file_url = '{file_url}'")
            uniq_click = len(all_about_file)
            all_click = 0
            for code in all_about_file:
                all_click += int(code[0])

            all_data_files = bms.all_data_files.split("-----")
            public_link = all_data_files[0]
            all_download = all_data_files[1]
            uniq_download = all_data_files[2]

            caption += f"\n\n{public_link} t.me/{bot_username}?start={file_url}\n\n<i>{all_download} </i><code>{all_click}</code>\n<i>{uniq_download}</i> <code>{uniq_click}</code>"
            try:
                await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                               caption=caption, parse_mode="html", reply_markup=await k.edit_file(bms))
            except:
                await call.answer(bms.no_changes)
        elif call.data == "delete":
            file_url = file["url"]
            await delete_db("files_click", f"file_url = '{file_url}'")
            await delete_db("files", f"file_url = '{file_url}'")
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            files_data = await select_db("*", "files", f"user_id = {call.message.chat.id}")
            caption = f"{bms.all_files}\n\n"
            for i in files_data:
                text = f"<a href='https://t.me/{bot_username}?start={i[4]}'>{i[7]}</a>\n\n"
                caption += text
            await bot.send_message(call.message.chat.id, caption, parse_mode="html")
        elif call.data == "i_agree":
            await of.edit_message(call.message.chat.id, call.message.message_id, file["caption"],
                                  k.add_description(bms))
        elif call.data == "do_not_agree":
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            url = file["url"]
            await delete_db("files", f"file_url = '{url}'")
    except IndexError:
        await bot.send_message(call.message.chat.id,
                               bms.sorry)


@dp.message_handler(content_types=CONTENT_TYPES)
async def what_message(message: types.Message):
    bms = Bmsg(message.from_user.language_code)
    global file
    global action, advertising, advertising_data

    if action == "pass" and advertising != "pass":
        if advertising == "photo":
            if message.text == "none":
                advertising = "text"
                await bot.send_message(chat_id=message.from_user.id, text="Ok, send me text")
            elif message.text == None and message.content_type == "photo":
                file_id = message["photo"][0].file_id
                advertising_data["photo"] = file_id
                advertising = "text"
                await bot.send_message(chat_id=message.from_user.id,
                                       text=f"{advertising_data}\n\nI'm save this photo. Ok, send me text")
            else:
                # print(message.text)
                advertising = "pass"
                await bot.send_message(message.from_user.id, "I don't know, bye!")
        elif advertising == "text":
            advertising_data["text"] = message.text
            advertising_data["entities"] = message['entities']
            advertising = "button"
            await bot.send_message(chat_id=message.from_user.id,
                                   text="<b>Ok, send me button example:</b>\n\n\nText button - https://t.me/CreateSuperBots\nNew text - https://t.me/csb_files_bot",
                                   disable_web_page_preview=True, parse_mode="html")
        elif advertising == "button":
            if len(message.text) > 20:
                try:
                    data = message.text.split("\n")
                    for i in data:
                        i = i.split(" - ")
                        advertising_data["button"]["text"].append(i[0])
                        advertising_data["button"]["link"].append(i[1])
                        advertising = "count"
                        await bot.send_message(chat_id=message.from_user.id,
                                               text="Отправь мне количество отправок или <code>all</code> для отправки всем",
                                               disable_web_page_preview=True, parse_mode="html")

                except IndexError as e:
                    advertising = "pass"
                    await bot.send_message(message.from_user.id, "I don't know, bye!")
            else:

                advertising = "pass"
                await bot.send_message(message.from_user.id, "I don't know, bye!")

        elif advertising == "count":
            try:
                advertising_data["count"] = int(message.text)
            except ValueError:
                if message.text == "all":
                    advertising_data["count"] = message.text
                else:
                    await bot.send_message(message.from_user.id, "Xyeta")
                advertising = "pass"

            if advertising_data['photo'] is not None:
                await bot.send_photo(chat_id=message.from_user.id, caption=advertising_data['text'],
                                     reply_markup=await keyboards.but_for_add(
                                         advertising_data["button"]["text"],
                                         advertising_data["button"]["link"],
                                         True, advertising_data["count"]),
                                     caption_entities=advertising_data["entities"],
                                     photo=advertising_data['photo'])
            else:
                await bot.send_message(chat_id=message.from_user.id, text=advertising_data['text'],
                                       reply_markup=await keyboards.but_for_add(
                                           advertising_data["button"]["text"],
                                           advertising_data["button"]["link"],
                                           True, advertising_data["count"]), disable_web_page_preview=True,
                                       entities=advertising_data["entities"])



    elif message.content_type == "text":
        if action == "add_description":
            file["dis"] = message.text
            url = file["url"]
            dis = file["dis"]
            await update_db("files", "description", f"'{dis}'", f"file_url = '{url}'")
            await of.send_file(message.from_user.id, file["url"], bms)
            action = "pass"
            file = {"url": file["url"], "dis": "", "name": "", "caption": ""}

        elif action == "edit_name":
            file["name"] = message.text
            url = file["url"]
            name = file["name"]
            await update_db("files", "file_name", f"'{name}'", f"file_url = '{url}'")
            await of.send_file(message.from_user.id, file["url"], bms)
            action = "pass"
            file = {"url": file["url"], "dis": "", "name": "", "caption": ""}


        else:
            text = str(bms.what)
            await bot.send_message(message.from_user.id, text=text)
    else:
        msg = await of.add_files(message, bms)
        file["url"] = msg[1]
        file["caption"] = msg[0]
        caption = msg[0]
        if msg[1] == "":
            await bot.send_message(message.from_user.id, caption, parse_mode="html")
        else:
            await bot.send_message(message.from_user.id,
                                   bms.attention,
                                   reply_markup=await k.i_agree(bms))


if __name__ == '__main__':
    executor.start_polling(dp)
