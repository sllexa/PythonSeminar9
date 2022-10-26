import telebot
from telebot import types
import requests
import json
import tictoc as tt

API_URL = "https://api.weather.yandex.ru/v2/informers?lat=55.75222&lon=37.61556"
headers = {"X-Yandex-API-Key": "********-eed2-456f-adaa-2e5812ec92c1"}

def get_token():
    with open('token.txt', 'r') as file:
        return file.read()

bot = telebot.TeleBot(get_token())

kb_game = types.InlineKeyboardMarkup()
kb_game.row(types.InlineKeyboardButton('1', callback_data='1'),
            types.InlineKeyboardButton('2', callback_data='2'),
            types.InlineKeyboardButton('3', callback_data='3'))
kb_game.row(types.InlineKeyboardButton('4', callback_data='4'),
            types.InlineKeyboardButton('5', callback_data='5'),
            types.InlineKeyboardButton('6', callback_data='6'))
kb_game.row(types.InlineKeyboardButton('7', callback_data='7'),
            types.InlineKeyboardButton('8', callback_data='8'),
            types.InlineKeyboardButton('9', callback_data='9'))

step = 0
pause_g = True
def run_game(chat_id):
    global step, pause_g
    game_over = False
    human = True
    str_mes = ""
    while game_over == False:
        pause_g = True
        bot.send_message(chat_id, tt.print_field())
    
        if human == True:
            symbol = "X"
            bot.send_message(chat_id, "Человек, ваш ход: ", reply_markup=kb_game)
            while pause_g:
                pass
        else:
            bot.send_message(chat_id, "Компьютер делает ход: ")
            symbol = "O"
            step = tt.AI()

        if step != "":
            tt.step_field(step,symbol) # делаем ход в указанную ячейку
            win = tt.get_result() # определим победителя
            if win != "":
                game_over = True
                str_mes = "Победитель " + win
            else:
                game_over = False
        else:
            str_mes = "Ничья! Победитела дружба"
            game_over = True
        human = not(human)        
    
    bot.send_message(chat_id, tt.print_field())
    bot.send_message(chat_id, f"{str_mes}")


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.username}!")

@bot.message_handler(commands=['game'])
def start_game(message):
    bot.send_message(message.chat.id, "Добро пожаловать в игру Крестики-нолики!\nПопробуй обыграть компьютер.")
    run_game(message.chat.id)

@bot.message_handler(commands=['get_weather', 'weather', 'pogoda'])
def get_weather(message):
    r = requests.get(url=API_URL, headers=headers)
    #bot.send_message(message.chat.id, r.text)
    if r.status_code == 200:
        data = json.loads(r.text)
        fact = data["fact"]
        bot.send_message(message.chat.id, text=f'Now in Moscow {fact["temp"]}°, feels like {fact["feels_like"]}°. Now on the street {fact["condition"]}')
    else:
        bot.send_message(message.chat.id, 'Problems on weather API')


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    global step, pause_g
    #bot.answer_callback_query(callback_query_id=call.id, text='Спасибо за честный ответ!')
    if call.data == '1': step = 1
    elif call.data == '2': step = 2
    elif call.data == '3': step = 3
    elif call.data == '4': step = 4
    elif call.data == '5': step = 5
    elif call.data == '6': step = 6
    elif call.data == '7': step = 7
    elif call.data == '8': step = 8
    elif call.data == '9': step = 9

    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    pause_g = False
  

bot.polling()