import telegram
import tokens
from telegram.ext import (Updater,
                          CommandHandler,
                          MessageHandler,
                          Filters,
                          InlineQueryHandler,
                          CallbackQueryHandler)
import logging
from awesome_filter import AwesomeFilter
import commands
import messages
import inline_queries
import callback_queries
import utils

def main():
    t_bot = telegram.Bot(token=tokens.EXTREPYTHON_BOT_TOKEN)
    print(t_bot.get_me())

    updater = Updater(token=tokens.EXTREPYTHON_BOT_TOKEN)

    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                         level=logging.INFO)

    awesome_filter = AwesomeFilter()

    start_command_handler = CommandHandler('start', commands.start)
    echo_handler = MessageHandler(Filters.text, messages.echo)
    caps_handler = CommandHandler('caps', commands.caps, pass_args=True)
    inline_caps_handler = InlineQueryHandler(inline_queries.inline_query)
    awesome_handler = MessageHandler(awesome_filter, messages.awesome_callback)
    callback_query_handler = CallbackQueryHandler(callback_queries.button)
    chat_id_handler = CommandHandler('chatId', commands.chat_id)
    inline_keyboard_handler = CommandHandler('keyboard', commands.inline_keyboard)
    timer_handler = CommandHandler('set', commands.set_timer, pass_args=True, pass_job_queue=True, pass_chat_data=True)
    unset_timer_handler = CommandHandler('unset', commands.unset, pass_chat_data=True)
    homer_handler = CommandHandler('homer', commands.homer)
    python_handler = CommandHandler('python', commands.python)
    emoji_handler = CommandHandler('emoji', commands.emoji, pass_args=True)
    unknown_handler = MessageHandler(Filters.command, utils.unknown)
    #echo_all_handler = MessageHandler(Filters.all, messages.echo_all, edited_updates=True)

    dispatcher.add_handler(start_command_handler)
    dispatcher.add_handler(awesome_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(caps_handler)
    dispatcher.add_handler(inline_caps_handler)
    dispatcher.add_handler(chat_id_handler)
    dispatcher.add_handler(callback_query_handler)
    dispatcher.add_handler(inline_keyboard_handler)
    dispatcher.add_handler(timer_handler)
    dispatcher.add_handler(unset_timer_handler)
    dispatcher.add_handler(homer_handler)
    dispatcher.add_handler(python_handler)
    dispatcher.add_handler(emoji_handler)
    dispatcher.add_handler(unknown_handler)
    #dispatcher.add_handler(echo_all_handler)

    updater.start_polling()

if __name__ == '__main__':
    main()


