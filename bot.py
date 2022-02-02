from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import aiogram
import time
import keyboards
import keyboards as k
import other_func as of
from db import *

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

CONTENT_TYPES = ["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact"]

file = {"url": "", "dis": "", "name": "", "caption": ""}

action = "pass"
advertising = "pass"
advertising_data = {"photo": None, "text": "", "entities": [], "button": {"text": [], "link": []}}


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
                                   "Этот бот предназначен для получения файлов. Поэтому сначала найди ссылку ну или отправь мне файл\n\n\nЕСЛИ ТЫ ОСТАНОВИШЬ ИЛИ ЗАБЛОКИРУЕШЬ БОТА\nВСЕ ТВОИ ФАЙЛЫ УДАЛЯТСЯ\nИ ССЫЛКИ СТАНУТ НЕДЕЙСТВИТЕЛЬНЫ\n🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺",
                                   reply_markup=await k.only_support())
    else:
        await bot.send_message(message.from_user.id,
                               "Этот бот предназначен для получения файлов. Поэтому сначала найди ссылку",
                               reply_markup=await k.only_support())


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
    await bot.send_message(message.from_user.id,
                           "Этот бот предназначен для получения файлов.\nМожешь мне отправить файл, а я дам ссылку\n\nЕсли что пиши @csb_support_bot",
                           parse_mode="html")


@dp.callback_query_handler()
async def callback_inline(call):
    try:
        global action
        global file

        if call.data == "confirm" and call.message.chat.username == "cha_artem":
            # print(call.message.chat.username)
            users_id = await select_db("user_id", "users")

            # print(users_id)
            for i in users_id:
                try:
                    await bot.send_photo(chat_id=i[0], caption=advertising_data['text'],
                                         reply_markup=await keyboards.but_for_add(advertising_data["button"]["text"],
                                                                                  advertising_data["button"]["link"]),
                                         caption_entities=advertising_data["entities"], photo=advertising_data['photo'])
                    time.sleep(0.5)
                except Exception :
                    await delete_db('files_click', f"user_id = {i[0]}")
                    await delete_db('files', f"user_id = {i[0]}")
                    await delete_db('users', f"user_id = {i[0]}")

        elif call.data == "delete_msg":
            await bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == "support":
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
            caption = f"<i>Название:</i> <code>{data_about_file[0][7]}</code>"  # \n\n<i>Описание: </i><code>{description}</code>"
            if description != "":
                caption += f"\n\n<i>Описание: </i><code>{description}</code>"
            all_about_file = await select_db("amount", "files_click", f"file_url = '{file_url}'")
            uniq_click = len(all_about_file)
            all_click = 0
            for code in all_about_file:
                all_click += int(code[0])
            caption += f"\n\nПубличная ссылка: t.me/{bot_username}?start={file_url}\n\n<i>Все скачивания: </i><code>{all_click}</code>\n<i>Уникальные скачивания:</i> <code>{uniq_click}</code>"
            try:
                await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                               caption=caption, parse_mode="html", reply_markup=await k.edit_file())
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
        elif call.data == "i_agree":
            await of.edit_message(call.message.chat.id, call.message.message_id, file["caption"], k.add_description())
        elif call.data == "do_not_agree":
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            url = file["url"]
            await delete_db("files", f"file_url = '{url}'")
            # await bot.send_message(call.message.chat.id, file["caption"], parse_mode="html",
            # reply_markup=await k.add_description())
    except IndexError:
        await bot.send_message(call.message.chat.id,
                               "Меня только что перезапустили, или возникла непредвиденая ситуация лучше об этом напиши @csb_support_bot")


@dp.message_handler(content_types=CONTENT_TYPES)
async def what_message(message: types.Message):
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
                print(message.text)
                advertising = "pass"
                await bot.send_message(message.from_user.id, "I don't know, bye!")
        elif advertising == "text":
            advertising_data["text"] = message.text
            # advertising_data["entities"] = dict(message)['entities']
            advertising_data["entities"] = message['entities']
            import json
            # print((dict(message)['entities'])) # todo: Сделал вытяжжку entities и 178 показано использование good night
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
                    await bot.send_photo(chat_id=message.from_user.id, caption=advertising_data['text'],
                                         reply_markup=await keyboards.but_for_add(advertising_data["button"]["text"],
                                                                                  advertising_data["button"]["link"],
                                                                                  True),
                                         caption_entities=advertising_data["entities"], photo=advertising_data['photo'])
                    # await bot.send_message(chat_id=message.from_user.id, text=advertising_data["text"],
                    # entities=advertising_data["entities"], reply_markup=await keyboards.but_for_add(advertising_data["button"]["text"], advertising_data["button"]["link"]))
                except IndexError as e:
                    advertising = "pass"
                    await bot.send_message(message.from_user.id, "I don't know, bye!")
            else:
                advertising = "pass"
                await bot.send_message(message.from_user.id, "I don't know, bye!")



    elif message.content_type == "text":
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
        file["caption"] = msg[0]
        caption = msg[0]
        if msg[1] == "":
            # await bot.send_message(message.from_user.id, caption, parse_mode="html",
            # reply_markup=await k.add_description())
            await bot.send_message(message.from_user.id, caption, parse_mode="html")
        else:
            await bot.send_message(message.from_user.id,
                                   """🛑 ВНИМАНИЕ | ATTENTION | УВАГА 📣\n️            ❗НАЗАР АУДАРЫҢЫЗ❗             \n\nОтправляя этот файл, вы берёте на себя ответственность за его распространение. Все последствия от использования данного файла владелец бота перекладывает на Вас.\n\nВы соглашаетесь?""",
                                   reply_markup=await k.i_agree())


if __name__ == '__main__':
    executor.start_polling(dp)
