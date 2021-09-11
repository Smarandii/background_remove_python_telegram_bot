from os import environ
from telebot import TeleBot
from telebot.types import Message
from dotenv import load_dotenv
import removebg

load_dotenv(".env")
bot = TeleBot(environ["API_KEY"])


class BotHelper:
    @staticmethod
    def delete_command(message: Message):
        slash_pos = message.text.find("/")
        return message.text[slash_pos::]


@bot.message_handler(commands=["start", "help"])
def start_message(message):
    bot.send_message(message.chat.id, "To use this bot for free, follow the instructions:\n"
                                      "0. Go to https://www.remove.bg/dashboard#api-key\n"
                                      "1. Get an API key in order to use remove.bg engine\n"
                                      "2. Send API key to this bot with command /set_api [YOUR API KEY]\n"
                                      "   Example: /send_api FA8YiwpnvBWPt2ap72go6UbA\n"
                                      "3. Send me some picture/document\n"
                                      "4. I will send this image back without background\n")


@bot.message_handler(commands=["send_api"], func=BotHelper.delete_command)
def receive_api(message):
    user_api = message.text
    # TODO: Write `user_api` to DB
    pass


@bot.message_handler(content_types=["photo"])
def get_photo(message):
    pass


@bot.message_handler(content_types=["document"])
def get_document(message):
    pass


if __name__ == '__main__':
    try:
        while True:
            bot.polling(none_stop=True)
    except Exception as e:
        print(e.args)








