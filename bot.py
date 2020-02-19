import time
import config
import random
import telebot
from telebot import types
import decorator

# pip install pytelegrambotapi

# https://stackoverflow.com/questions/42796300/get-photo-in-telegram-bot-through-pytelegrambotapi/46242244
# https://www.programcreek.com/python/example/94889/telebot.TeleBot
# https://stackoverflow.com/questions/10607688/how-to-create-a-file-name-with-the-current-date-time-in-python

# ein bot-object wird erstellt

# data
part1=["Putin", "Hillary", "Obama", "Fake News", "Mexico", "Arnold Schwarzenegger", "Democrats", "Xi Jinping", "Angela Merkel", "Jeff Bezos", "Bill Gates", "Emmanuel Macron", "Mark Zuckerberg", "Warren Buffett", "Jack Ma"]
part2=["no talen", "on the way down", "really poor numbers", "nasty tone", "looking like a fool", "bad hombre"]
part3=["got destroyed by my ratings.", "regged the election.", "had a much smaller crowd.", "will pay for the wall."]
part4=["So sad", "Apologize", "So true", "Media won't report", "Can you believe that?", "We have to make America great again!", "I don't believe in that", "Big trouble", "Fantastic job", "Stay tuned", "Believe me", "Work hard", "Right?", "Political correctness is killing our country", "Drain the Swamp", "Don’t worry, we will win!", "Be brutal, be tough", "Really bad people!"]

bot = telebot.TeleBot(config.TOKEN)

@decorator.decorator
def errLog(func, *args, **kwargs):
    result = None
    try:
        result = func(*args, **kwargs)
    except Exception as e:
        print(f"88. e.__repr__(): {e.__repr__()}")
    return result

@bot.message_handler(commands=['start'])
def welcome(message):

    sti = open('static/trump.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    # photo select für den bot
    # pho = open('static/test_003.jpg', 'rb')
    # bot.send_photo(message.chat.id, pho)

    # keyboard select für den bot

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item_1 = types.KeyboardButton("🎲 random number")
    item_2 = types.KeyboardButton("😊 How are you?")

    markup.add(item_1, item_2)

    bot.send_message(message.chat.id, "Welcome back, {0.first_name}!\nIch bin - <b>{1.first_name}</b>, der Trump-Bot.".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == '🎲 random number':

            random.seed()

            bot.send_message(message.chat.id, str(random.randint(0,100)))

        elif message.text == '😊 How are you?':

            markup = types.InlineKeyboardMarkup(row_width=3)
            item_1 = types.InlineKeyboardButton("I'am fine!", callback_data='good')
            item_2 = types.InlineKeyboardButton("It could be better...", callback_data='bad')

            markup.add(item_1, item_2)
            bot.send_message(message.chat.id, 'Very good and you?', reply_markup=markup)

        else:

            random.seed()

            # output
            ending = random.choice(part4)

            if ending[-1] != ( '?' or '!' ):
                ending = ending + "."

            bot.send_message(message.chat.id, random.choice(part1) + " " + random.choice(part2) + " " + random.choice(part3) + " " + ending )

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'That pleases me! Keep it up! 😊')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Can happen, be strong! 😢')
            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="👇", reply_markup=None)
            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Huhu - I'm up here!")

    except Exception as e:
        print(f"666. repr(e): {repr(e)}")

@errLog
def processPhotoMessage(message):
    print(f"01. message.photo: {message.photo}")
    fileID = message.photo[-1].file_id
    print(f"02. fileID ={fileID}")
    file = bot.get_file(fileID)
    print(f"03. file.file_path: {file.file_path}\n")
    print(f"04. file.file_path: {bot.get_file(fileID).file_path}\n")
    downloaded_file = bot.download_file(file.file_path)
    with open("image_" + time.strftime('%Y%m%d-%H%M%S') + ".jpg", 'wb') as new_file:
        new_file.write(downloaded_file)

@bot.message_handler(content_types=['photo'])
def photo(message):
    processPhotoMessage(message)

# RUN
bot.polling(none_stop=True)
