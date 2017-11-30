from telegram import InlineQueryResultArticle, InputTextMessageContent, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from uuid import uuid4
from telegram.utils.helpers import escape_markdown

def alarm(bot, job):
    bot.send_message(job.context, text='Beep!')

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hola mundo, soy un bot, por favor, háblame!!")

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)

def inline_query(bot, update):
    query = update.inline_query.query
    if not query:
        return
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Caps",
            input_message_content=InputTextMessageContent(
                query.upper())),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Bold",
            input_message_content=InputTextMessageContent(
                "*{}*".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN)),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Italic",
            input_message_content=InputTextMessageContent(
                "_{}_".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN))]
    bot.answer_inline_query(update.inline_query.id, results)

def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Lo siento, no entiendo ese comando :(')

def callback_minute(bot, chat_id):
    bot.send_message(chat_id='-265182967', text='En un minuto vuelvo')

def awesome_callback(bot, update):
    update.message.reply_text('¿Hablas tu de ExtrePython? La mejor comunidad de Python de España Hulio')

def chat_id(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='El idenficador de este chat es ' + str(update.message.chat_id))

def inline_keyboard(bot, update):
    keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
                 InlineKeyboardButton("Option 2", callback_data='2')],
                [InlineKeyboardButton("Option 3", callback_data='3')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def button(bot, update):
    query = update.callback_query
    bot.edit_message_text(text="Selected option: {}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

def set_timer(bot, update, args, job_queue, chat_data):
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(args[0])
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return

        # Add job to queue
        job = job_queue.run_repeating(alarm, due, context=chat_id)
        chat_data['job'] = job

        update.message.reply_text('Timer successfully set!')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')

def unset(bot, update, chat_data):
    """Remove the job if the user changed their mind."""
    if 'job' not in chat_data:
        update.message.reply_text('You have no active timer')
        return

    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']

    update.message.reply_text('Timer successfully unset!')

import telegram
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import InlineQueryHandler
from telegram.ext import CallbackQueryHandler
from awesome_filter import AwesomeFilter

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

#Filters.video, Filters.photo
awesome_filter = AwesomeFilter()

start_command_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text, echo)
caps_handler = CommandHandler('caps', caps, pass_args=True)
inline_caps_handler = InlineQueryHandler(inline_query)
unknown_handler = MessageHandler(Filters.command, unknown)
awesome_handler = MessageHandler(awesome_filter, awesome_callback)
chat_id_handler = CommandHandler('chatId', chat_id)
inline_keyboard_handler = CommandHandler('keyboard', inline_keyboard)
timer_handler = CommandHandler('set', set_timer, pass_args=True, pass_job_queue=True, pass_chat_data=True)
unset_timer_handler = CommandHandler('unset', unset, pass_chat_data=True)

job_minute = job_queue.run_repeating(callback_minute, interval=60, first=0)

dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(awesome_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(caps_handler)
dispatcher.add_handler(inline_caps_handler)
dispatcher.add_handler(chat_id_handler)
dispatcher.add_handler(CallbackQueryHandler(button))
dispatcher.add_handler(inline_keyboard_handler)
dispatcher.add_handler(timer_handler)
dispatcher.add_handler(unset_timer_handler)
dispatcher.add_handler(unknown_handler)

