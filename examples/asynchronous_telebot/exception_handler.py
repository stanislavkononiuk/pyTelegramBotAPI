
import telebot
from telebot.async_telebot import AsyncTeleBot


import logging

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

class ExceptionHandler(telebot.ExceptionHandler):
    def handle(self, exception):
        logger.error(exception)

bot = AsyncTeleBot('TOKEN',exception_handler=ExceptionHandler())




@bot.message_handler(commands=['photo'])
async def photo_send(message: telebot.types.Message):
    await bot.send_message(message.chat.id, 'Hi, this is an example of exception handlers.')
    raise Exception('test') # Exception goes to ExceptionHandler if it is set
    


bot.polling(skip_pending=True)
