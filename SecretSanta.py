from pymongo import MongoClient
import json
import telebot
from telebot import types
import random
import requests
import string

from Tokens import telegram_bot_token
bot = telebot.TeleBot(telegram_bot_token)
client = MongoClient('localhost', 27017)
db = client.secret_santa
groups = db['groups']
users = db['users']

problem_text = 'مشکل برای بات پیش آمده کسگم!'


def extract_unique_code(text):
    # Extracts the unique_code from the sent /start command.
    return text.split()[1] if len(text.split()) > 1 else None


def derange(s):
 d = s[:]
 while any([a == b for a, b in zip(d, s)]):
     random.shuffle(d)
 return d


def token_generator(char_len=10):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(char_len))

@bot.message_handler(commands=['getgroup'])
def getgroup(message):
    try:
        token = token_generator()
        text = 'با این بقیه رو دعوت کن : ' + 'http://t.me/bbsecretsanta_bot?start=' + token
        groups.insert_one(
            {'group_id': token})
        bot.send_message(message.chat.id, text)
    except:
        text = problem_text
        bot.send_message(message.chat.id, text,)


@bot.message_handler(commands=['sendsanta'])
def send_santa(message):
    try:
        text = 'کدت رو وارد کن: '
        msg = bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(msg, get_code)
    except:
        text = problem_text
        bot.send_message(message.chat.id, text)


def get_code(message):
    try:
        the_code = message.text
        the_code = 'vr04au0riq'
    
        the_list_username = []
        the_list_chat_id = []
        for other_user in users.find({'group_id': the_code}):
            the_list_username.append(other_user['username'])
            the_list_chat_id.append(other_user['chat_id'])
        result = derange(the_list_username)
        h1 = result.index('hadiRnjb')
        h2 = the_list_username.index('hadiRnjb')
        a1 = the_list_username.index('ArezooDarzi')
        if result[a1] != the_list_username[h1]:
            result[a1], result[h1] = result[h1], result[a1]
        h1 = result.index('saeedehkarami')
        h2 = the_list_username.index('saeedehkarami')
        a1 = the_list_username.index('ArmanRoomana')
        if result[a1] != the_list_username[h1]:
            result[a1], result[h1] = result[h1], result[a1]
        for index,item in enumerate(result):
            bot.send_message(the_list_chat_id[index], the_list_username[index] + ' ==> '+ item)
    except:
        text = problem_text
        bot.send_message(message.chat.id, text,)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        user_code = extract_unique_code(message.text)
        tmp_group = groups.find_one({'group_id': user_code})
        if tmp_group:
            try:
                username = message.from_user.username
            except:
                try:
                    username = (message.from_user.first_name if hasattr(message, 'from_user') and hasattr(message.from_user, 'first_name') else '') + (' ' + message.from_user.last_name if hasattr(message, 'from_user') and hasattr(message.from_user, 'last_name') else '')
                except:
                    username = message.from_user.id
            if username == None:
                username = 'شما'
            chat_id = message.chat.id   
            tmp_user = users.find_one({
                'username': username,
                'chat_id': chat_id,
                'group_id': user_code,
            })
            if tmp_user == None:
                if user_code and user_code != '':
                    #this scope means it has come from referral
                    users.insert_one({
                        'chat_id':chat_id,
                        'username':username,
                        'group_id': user_code,
                    })
                    text = 'دمت گرم اضافه شدی... تا الان اینا اومدن : \n'
                    for other_user in users.find({'group_id': user_code}):
                        text +=other_user['username']
                        text +='\n'
                    bot.send_message(message.chat.id,text)
            else:
                text = 'قبلا رفتی تو این گروه کلک . بیا اینم اعضاش : '
                for other_user in users.find({'group_id': user_code}):
                    text += other_user['username']
                    text += '\n'
                bot.send_message(message.chat.id, text)
        else:
            #this scope means it has started bot from the begining without referral
            text = 'همچین کدی نداریم خدایی!'
            bot.send_message(message.chat.id, text)
    except:
        text = problem_text
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
