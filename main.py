from flibusta import flib as flibusta
import os
from telebot import types
import telebot

token = open('settings/token.txt').readline()
bot = telebot.TeleBot(token)  # инит
admin = open('settings/admin.txt').readline() # админ


@bot.message_handler(commands=['start', 'help'])  # старт
def send_welcome(message):
    usr_id = str(message.from_user.id)  # userid
    usr_name = str(message.from_user.first_name)  # имя юзера
    keyboard = types.ReplyKeyboardMarkup(True)  # генерируем клаву
    butt_findbook = types.KeyboardButton(text='Поиск книги')
    keyboard.add(butt_findbook)
    bot.reply_to(message, "Привет, " + str(message.from_user.first_name), reply_markup=keyboard)  # здороваемся
    bot.reply_to(message, "Я - крутой и милый бот. Умею искать книжки на Флибусте и присылать тебе в формате fb2. Меня создал @mihailovily, по любым вопросам пиши ему.")


@bot.message_handler(commands=['find'])
@bot.message_handler(regexp="Поиск книги")
def find(message):
    bot.reply_to(message, 'Введите название книги для поиска')
    bot.register_next_step_handler(message, result_back)
    # кушаем ответ, пихаем в след функцию


def statuscheck():
    a = open('log.txt').readlines()
    return a


def result_back(message):
    if message.text != '/find':
        bot.reply_to(message, 'Поиск')
        book_name = flibusta.cli(message.text)
        usr_id = str(message.from_user.id)
        
        if statuscheck() == ['ok\n']:
            document = open('book.fb2', 'rb')
            bot.send_document(usr_id, document)  # отвечаем треком, пихаем в него метаданные (*)
            os.system('rm book.fb2')
            bot.send_message(usr_id, 'Книга "' + book_name + '" загружена. Приятного чтения!')
        else:
            bot.reply_to(message, 'По вашему запросу не найдено ни одной книги')
        os.system('rm log.txt')

# если сообщение не распознано
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, 'Я тебя не понял')


if __name__ == '__main__':
    bot.infinity_polling()
