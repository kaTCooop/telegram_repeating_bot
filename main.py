# module name pyTelegramBotAPI, import as telebot

import telebot
import config
import random
import sqlite3
import os

from telebot import types
from requests.exceptions import ReadTimeout, ConnectionError
from http.client import RemoteDisconnected
from urllib3.exceptions import ProtocolError
from telebot.apihelper import ApiTelegramException

bot = telebot.TeleBot(config.TOKEN)

# keyboard
markup = types.ReplyKeyboardMarkup(resize_keyboard=True) # resize - small keyboard
item1 = types.KeyboardButton('Random number 0-100')
markup.add(item1)

def get_user_ids(db):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Users')
    users = cursor.fetchall()
    ids = []

    for user in users:
        ids.append(user[0])
    
    connection.close()
    return ids

def insert_text(id, text, db):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    cursor.execute(f'INSERT INTO user{str(id)} (message) VALUES (?)', (text,))

    connection.commit()
    connection.close()

def insert_user(id, username, db):
    ids = get_user_ids(db)

    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    if int(id) not in ids:
        cursor.execute('INSERT INTO Users (id, username) VALUES (?, ?)', (id, username))

    connection.commit()
    connection.close()

@bot.message_handler(commands=['start'])
def welcome(message):
    insert_user(message.chat.id, message.from_user.username, 'database.db')

    sti = open('static/welcome.webm', 'rb')
    bot.send_sticker(message.chat.id, sti)

    bot.send_message(message.chat.id, 'Welcome, {0.first_name}!\nI am - <b>{1.first_name}</b>, test bot'.format(message.from_user, bot.get_me()), 
                     parse_mode='html', reply_markup=markup)
    
    insert_text(message.chat.id, message.text, 'database.db')

    print(message.chat.id, '{0.username}:'.format(message.from_user), message.text)

@bot.message_handler(content_types=['text'])
def lalala(message):
    insert_user(message.chat.id, message.from_user.username, 'database.db')

    if message.text == 'Random number 0-100':
        bot.send_message(message.chat.id, str(random.randint(0, 101)))
    
    else:
        bot.send_message(message.chat.id, message.text, reply_markup=markup)
    
    insert_text(message.chat.id, message.text, 'database.db')

    print(message.chat.id,'{0.username}:'.format(message.from_user), message.text)

@bot.message_handler(content_types=['sticker'])
def lalala_sticker(message):
    insert_user(message.chat.id, message.from_user.username, 'database.db')

    bot.send_sticker(message.chat.id, message.sticker.file_id, reply_markup=markup)
    insert_text(message.chat.id, f'sticker id: {message.sticker.file_id}', 'database.db')

    print(message.chat.id,'{0.username}:'.format(message.from_user), 'sticker id:', message.sticker.file_id)

@bot.message_handler(content_types=['photo'])
def lalala_image(message):
    insert_user(message.chat.id, message.from_user.username, 'database.db')

    bot.send_photo(message.chat.id, photo=message.photo[-1].file_id, reply_markup=markup)
    insert_text(message.chat.id, f'photo id: {message.photo[-1].file_id}', 'database.db')

    print(message.chat.id,'{0.username}:'.format(message.from_user), 'photo id:', message.photo[-1].file_id)


connection = sqlite3.connect('database.db')
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL
)
''')

ids = get_user_ids('database.db')

for id in ids:
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS user{str(id)} (
    message TEXT NOT NULL
    )
    ''')

connection.commit()
connection.close

# RUN
try:
	bot.polling(none_stop=True)

except (ReadTimeout, ConnectionError, RemoteDisconnected, ProtocolError, ApiTelegramException):
    if a == 'ApiTelegramException':
        print('bad gateway')
    else:
        os.execv(sys.argv[0], sys.argv)

