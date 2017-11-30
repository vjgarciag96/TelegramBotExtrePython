def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

def awesome_callback(bot, update):
    update.message.reply_text('¿Hablas tu de ExtrePython? La mejor comunidad de Python de España Hulio')

