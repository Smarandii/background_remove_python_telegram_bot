from os import environ, mkdir, path
from telebot import TeleBot
from telebot.types import Message
from dotenv import load_dotenv
from db import DataBase
from mocks import User
from removebg.removebg import RemoveBg


class BotHelper:
    load_dotenv(".env")
    bot = TeleBot(environ["API_KEY"])
    db = DataBase()

    def __init__(self):
        pass

    @staticmethod
    def delete_command(message: Message):
        space_pos = message.text.find(" ")
        message.text = message.text[space_pos + 1::]
        return message


@BotHelper.bot.message_handler(commands=["start", "help"])
def start_message(message):
    BotHelper.bot.send_message(message.chat.id, "To use this bot for free, follow the instructions:\n\n"
                                      "0. Go to https://www.remove.bg/dashboard#api-key\n"
                                      "1. Get an API key in order to use remove.bg engine\n\n"
                                      "2. Send API key to this bot with command /set_api [YOUR API KEY]\n\n"
                                      "Example:\n /send_api FA8YiwpnvBWPt2ap72go6UbA\n\n"
                                      "3. Send me some image without compression\n"
                                      "4. I will send this image back without background\n",
                               disable_web_page_preview=True)
    user = User(message=message)
    if BotHelper.db.user_not_exist(user):
        BotHelper.db.add(user)
    else:
        print("USER ALREADY IN DB")


@BotHelper.bot.message_handler(commands=["send_api"], func=BotHelper.delete_command)
def receive_api(message):
    user = User(message=message)
    user = BotHelper.db.find(user)
    user.api_key = message.text
    BotHelper.db.update(user)
    print("USER API KEY UPDATED:", user.__repr__())
    BotHelper.bot.send_message(user.tg_id, "API KEY received!")


@BotHelper.bot.message_handler(content_types=["photo"])
def get_photo(message):
    BotHelper.bot.reply_to(message, "Send it without compression!")


@BotHelper.bot.message_handler(content_types=["document"])
def get_document(message):
    try:
        mkdir(f"{message.chat.id}")
    except FileExistsError:
        pass
    try:
        user = BotHelper.db.find(User(tg_id=message.chat.id))
        if user.api_key is not None:
            rb = RemoveBg(api_key=user.api_key, error_log_file=".log")
            BotHelper.bot.send_chat_action(message.chat.id, 'typing', timeout=5)
            file_id_info = BotHelper.bot.get_file(message.document.file_id)
            downloaded_file = BotHelper.bot.download_file(file_id_info.file_path)
            file_path = path.join(f"{message.chat.id}", f'no_background.png')
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            BotHelper.bot.reply_to(message, "Photo downloaded and ready!")
            rb.remove_background_from_img_file(file_path)
            BotHelper.bot.send_document(user.tg_id, open(file_path, "rb"))
    except Exception as ex:
        BotHelper.bot.send_message(message.chat.id, f"Something bad just happened! Please check your api key. "
                                          f"Revoke and create again.")
        BotHelper.bot.send_message(message.chat.id, f"{ex}")
        print(f"[!] document generation error - {ex}")


if __name__ == '__main__':
    try:
        while True:
            BotHelper.bot.polling(none_stop=True)
    except Exception as e:
        print(e.args)








