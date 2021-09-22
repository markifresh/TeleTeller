from flask import Flask, request
from emojis.db.db import EMOJI_DB
from random import choice, choices
from os import getenv
import telebot
from pathlib import Path

TOKEN = getenv("TOKEN")
PORT = getenv("APP_PORT")
HOST = getenv("HOST")
HOOK_ADDRESS = getenv("HOOK_ADDRESS")
emojis_icons = [emoj.emoji for emoj in EMOJI_DB if emoj.unicode_version not in ("11.0", "12.0", "13.0")]

bot = telebot.TeleBot(token=TOKEN)

# removes hooks for current application
if not bot.set_webhook(url=''):
    exit(606)

# set up a new hook
web_hook = bot.set_webhook(url=f'{HOOK_ADDRESS}/{TOKEN}', certificate=Path('cert.pem').read_bytes())
if not web_hook:
    exit(707)

emoji_length_options = ('4', '6', '9')

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message,
                 ("Hi there!\n"
                  "I am the bot, who tells you stories."))



keyboard1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard1.row(*emoji_length_options)

@bot.message_handler(content_types=['text'])
def send_story(message):
    if message.text.isdigit():
        if message.text in emoji_length_options:
            emoji_length = int(message.text)
            mess = ''.join(choices(emojis_icons, k=emoji_length))
            bot.send_message(message.chat.id, mess, reply_markup=keyboard1)
        else:
            bot.reply_to(message, 'Noooo, I can not like this... better to choose', reply_markup=keyboard1)
    elif '?' in message.text:
        bot.send_message(message.chat.id, choice(emojis_icons), reply_markup=keyboard1)
    else:
        bot.reply_to(message,
                         text='Wait a second... I can only:\n'
                              '1) Show you a story\n'
                              '2) Answer to your question',
                         reply_markup=keyboard1)




app = Flask(__name__)

@app.route(f'/{TOKEN}', methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return 'ok'


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, threaded=True, ssl_context=('cert.pem', 'key.pem'))
