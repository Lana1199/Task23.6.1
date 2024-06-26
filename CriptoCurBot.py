
import telebot
from config import keys, TOKEN
from extensions import CriptoConverter,APIExcetion

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = (' Чтобы начать работу, введите боту команду в следующем формате:\n <имя валюты>\
<в какую перевести>\
<количество переводимой валюты>\nСмотреть список всех доступных валют:/values')

    bot.reply_to(message,text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text,key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text',])
def get_price(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIExcetion('Слишком много\мало параметров')

        quote, base, amount = values
        total_base = CriptoConverter.get_price(quote, base, amount)
    except APIExcetion as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')

    except Exception as e:
        bot.reply_to(message,f'Не удалось обработать команду\n{e}')
    else:
        text = f'Переводим {quote} в {base}\n{amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id,text)


bot.polling()


