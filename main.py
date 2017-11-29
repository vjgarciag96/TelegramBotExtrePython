from telegram import InlineQueryResultArticle, InputTextMessageContent

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hola mundo, soy un bot, por favor, háblame!!")

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)

def inline_caps(bot, update):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    bot.answer_inline_query(update.inline_query.id, results)

def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Lo siento, no entiendo ese comando :(')

def callback_minute(bot, job):
    bot.send_message(chat_id='187395179', text='En un minuto vuelvo')


import telegram
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import InlineQueryHandler

import logging
import tokens

t_bot = telegram.Bot(token=tokens.EXTREPYTHON_BOT_TOKEN)
print(t_bot.get_me())

updater = Updater(token=tokens.EXTREPYTHON_BOT_TOKEN)
updater.start_polling()
dispatcher = updater.dispatcher
job_queue = updater.job_queue
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

start_command_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text, echo)
caps_handler = CommandHandler('caps', caps, pass_args=True)
inline_caps_handler = InlineQueryHandler(inline_caps)
unknown_handler = MessageHandler(Filters.command, unknown)

job_minute = job_queue.run_repeating(callback_minute, interval=60, first=0)

dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(caps_handler)
dispatcher.add_handler(inline_caps_handler)
dispatcher.add_handler(unknown_handler)