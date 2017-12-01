from telegram.ext import BaseFilter

class AwesomeFilter(BaseFilter):
    def filter(self, message):
        if message.text:
            return 'extrepython' in message.text