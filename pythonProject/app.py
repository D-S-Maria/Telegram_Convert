import telebot

from config import TOKEN, keys
from extensions import APIException, Convertion

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате' \
           '\n <имя валюты> <в какую валюту перевести> <количсетво переводимой валюты>' \
           '\n чтобы узнать доступные валюты для перевода введите команду /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for val in keys.values():
        text = '\n'.join((text, val[0],))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        text = message.text.split()
        if len(text) != 3:
            raise APIException('Неверное количество параметров')
        v1, v2, n = text
        f, v1, v2 = Convertion.get_price(v1, v2, n)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя: {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду: {e}')
    else:
        bot.reply_to(message, f'{n} {v1} = {f} {v2}')


bot.polling()
