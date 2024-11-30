import telebot
import config

bot = telebot.TeleBot(config.TOKEN)

id = '123891'

while True:
    a = input('send reply: ')

    if a is not None:
        bot.send_message(id, a)

    else:
        continue

