from telegram import (InlineKeyboardButton,
                      InlineKeyboardMarkup)
from random import randint
from emoji import emojize
import constants

def alarm(bot, job):
    bot.send_message(job.context, text='Beep!')

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hola mundo, soy un bot, por favor, háblame!!")

def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)

def chat_id(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='El idenficador de este chat es ' + str(update.message.chat_id))

def inline_keyboard(bot, update):
    keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
                 InlineKeyboardButton("Option 2", callback_data='2')],
                [InlineKeyboardButton("Option 3", callback_data='3')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def set_timer(bot, update, args, job_queue, chat_data):
    chat_id = update.message.chat_id
    try:
        due = int(args[0])
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return

        job = job_queue.run_repeating(alarm, due, context=chat_id)
        chat_data['job'] = job

        update.message.reply_text('Timer successfully set!')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')

def unset(bot, update, chat_data):
    if 'job' not in chat_data:
        update.message.reply_text('You have no active timer')
        return

    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']

    update.message.reply_text('Timer successfully unset!')

def homer(bot, update):
    bot.send_photo(chat_id=update.message.chat_id, photo=constants.HOMER_IMAGES[randint(0, constants.HOMER_IMAGES.__len__()-1)])

def python(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='🐍🐍🐍🐍🐍🐍')

def emoji(bot, update, args):
    bot.send_message(chat_id=update.message.chat_id, text=emojize(':'+str(args[0])+':', use_aliases=True))