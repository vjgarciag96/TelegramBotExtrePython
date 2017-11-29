import telegram
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters

import logging

import tokens


t_bot = telegram.Bot(token=tokens.EXTREPYTHON_BOT_TOKEN)
print(t_bot.get_me())

updater = Updater(token=tokens.EXTREPYTHON_BOT_TOKEN)
updater.start_polling()
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hola mundo, soy un bot, por favor, háblame!!")

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)

start_command_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text, echo)
caps_handler = CommandHandler('caps', caps, pass_args=True)

dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(caps_handler)