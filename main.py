import telebot
import db
import urllib
import os
import json
from botData import token
from botImage import get_blob

bot = telebot.TeleBot(token)

def get_response(url):
	operUrl = urllib.request.urlopen(url)
	if(operUrl.getcode()==200):
		data = operUrl.read()
		jsonData = json.loads(data)
	else:
		print("Error receiving data", operUrl.getcode())
	return jsonData

def convert_to_blob(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data

@bot.message_handler(commands=['start'])
def starting(message):
	global user
	user = []
	curr_id = message.from_user.id
	user.append(curr_id)
	bot.send_message(message.chat.id, "Привет студент! Как подготовка? Если ты хочешь найти единомышленников, давай познакомимся !")
	send = bot.send_message(message.chat.id, "Как мне тебя звать ?")
	bot.register_next_step_handler(send, get_name)

def get_name(message):
	user.append(message.text)
	send = bot.send_message(message.chat.id, "В какой стране ты живёшь? Буду рад если напишешь дополнительно свой город!)")
	bot.register_next_step_handler(send, get_location)

# def get_year(message):
# 	user.append(message.text)
# 	send = bot.send_message(message.chat.id, "What's your gender?")
# 	bot.register_next_step_handler(send, get_gender)

# def get_gender(message):
# 	user.append(message.text)
# 	send = bot.send_message(message.chat.id, "В какой стране ты живёшь? Буду рад если напишешь дополнительно свой город!)")
# 	bot.register_next_step_handler(send, get_location)

def get_location(message):
	user.append(message.text)
	send = bot.send_message(message.chat.id, "Что ты можешь рассказать о себе? К чему ты готовишься ? Экзамены или Университеты ?")
	bot.register_next_step_handler(send, get_info)

def get_info(message):
	user.append(message.text)
	# send = bot.send_message(message.chat.id, "Send me an image")
	send = bot.send_message(message.chat.id, "Отправь мне свою фотографию, или любую иллюстрацию которая идентифицирует тебя!)")
	bot.register_next_step_handler(send, get_photo)

def get_photo(message):
	id = message.photo[0].file_id
	print(id)
	user.append(get_blob(id))
	send = bot.send_message(message.chat.id, "Мы всё настроили, теперь полетели ")
	query_add_user = "REPLACE INTO users(id) VALUES (%s)"
	query_add_form = "REPLACE INTO forms(id, name, city, info, image) VALUES (%s, %s, %s, %s, %s)"
	# id name city info photo
	db.tgbot.execute(query_add_user, user)
	db.tgbot.execute(query_add_form, user)
	db.connection.commit()

# @bot.message_handler(commands=['all'])
# def show_all(message):
# 	query_find_me = "SELECT * FROM users"
# 	db.tgbot.execute(query_find_me)
# 	result = db.tgbot.fetchall()
# 	for row in result:
# 		print(row)

@bot.message_handler(commands=['find'])
def show_one(message):
	query_find_me = "SELECT name, city, info, photo FROM users ORDER BY RAND() LIMIT 1"
	db.tgbot.execute(query_find_me)
	result = db.tgbot.fetchall()
	row = result[0]
	bot.send_message(message.chat.id, row[0] + " из " + row[1])
	bot.send_message(message.chat.id, row[2])
	bot.send_photo(message.chat.id, row[3])


bot.polling()