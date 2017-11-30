from telegram.ext import BaseFilter

class AwesomeFilter(BaseFilter):
    def filter(self, message):
        return 'extrepython' in message.text