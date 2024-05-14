import telebot
from currency_converter import CurrencyConverter
from telebot import types

bot = telebot.TeleBot('6846918378:AAEWoUZUwT6oxm4bhXpiouulzJT-ydULcWU')
currency = CurrencyConverter()
amount = 0


@bot.message_handler()
def start(message):
    bot.send_message(message.chat.id, 'Привет! Введите сумму')
    bot.register_next_step_handler(message, summa)


def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат. Впишите сумму')
        bot.register_next_step_handler(message, summa)
        return
    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('RUB/KGS', callback_data='RUB/KGS')
        btn2 = types.InlineKeyboardButton('KGS/RUB', callback_data='KGS/RUB')
        btn3 = types.InlineKeyboardButton('KGS/KZT', callback_data='KGS/KZT')
        btn4 = types.InlineKeyboardButton('Другое значение', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Число должно быть больше за 0. Впишите сумму')
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'{amount} равен {round(res,2)}. Можете заново вписать сумму')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, "Введите пару значений через слэш")
        bot.register_next_step_handler(call.message, my_currency)

def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'{amount} равен {round(res, 2)}. Можете заново вписать сумму')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, f'Значения должны быть в формате "значение/значение"')
        bot.register_next_step_handler(message, my_currency)

bot.polling(none_stop=True)
