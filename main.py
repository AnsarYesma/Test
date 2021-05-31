import telebot
from db import *
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

@bot.message_handler(commands=['start'])
def starting(message):
	global user
	user = []
	curr_id = message.chat.id
	user.append(curr_id)
	query_checkFirst = """
	SELECT id FROM tgbot.users WHERE id = %s
	""" % curr_id
	tgbot.execute(query_checkFirst)
	res = tgbot.fetchall()
	if len(res) == 0:
		bot.send_message(message.chat.id, "Привет студент! Как подготовка? Если ты хочешь найти единомышленников, давай познакомимся !")
	else:
		bot.send_message(message.chat.id, "Привет студент! Хочешь поменять анкету? Для отмены можешь отправить 'Отмена' на любом вопросе.")
	send = bot.send_message(message.chat.id, "Как мне тебя звать ?")
	bot.register_next_step_handler(send, get_name)

# DEBUG PART
@bot.message_handler(commands=['debug'])
def starting(message):
	global user
	user = []
	curr_id = int(input("ID_debug: "))
	user.append(curr_id)
	query_checkFirst = """
	SELECT id FROM tgbot.users WHERE id = %s
	""" % curr_id
	tgbot.execute(query_checkFirst)
	res = tgbot.fetchall()
	if len(res) == 0:
		bot.send_message(message.chat.id, "Привет студент! Как подготовка? Если ты хочешь найти единомышленников, давай познакомимся !")
	else:
		bot.send_message(message.chat.id, "Привет студент! Хочешь поменять анкету? Для отмены можешь отправить 'Отмена' на любом вопросе.")
	send = bot.send_message(message.chat.id, "Как мне тебя звать ?")
	bot.register_next_step_handler(send, get_name)
# DEBUG PART
def get_name(message):
	if (message.text == 'Отмена'):
		return
	user.append(message.text)
	send = bot.send_message(message.chat.id, "В каком городе ты живёшь?")
	bot.register_next_step_handler(send, get_location)

def get_location(message):
	if (message.text == 'Отмена'):
		return
	user.append(message.text)
	send = bot.send_message(message.chat.id, "Что ты можешь рассказать о себе? К чему ты готовишься ? Экзамены или Университеты ?")
	bot.register_next_step_handler(send, get_info)

def get_info(message):
	if (message.text == 'Отмена'):
		return
	user.append(message.text)
	# send = bot.send_message(message.chat.id, "Send me an image")
	send = bot.send_message(message.chat.id, "Отправь мне свою фотографию, или любую иллюстрацию которая идентифицирует тебя!)")
	bot.register_next_step_handler(send, get_photo)

def get_photo(message):
	if (message.text == 'Отмена'):
		return
	id = message.photo[0].file_id
	# print(id)
	user.append(get_blob(id))
	query_add_user = "REPLACE INTO users(id) VALUES (%s)"
	query_add_form = "REPLACE INTO forms(id, name, city, info, image) VALUES (%s, %s, %s, %s, %s)"
	# id name city info photo
	temp = []
	temp.append(user[0])
	tgbot.execute(query_add_user, temp)
	tgbot.execute(query_add_form, user)
	connection.commit()
	user.clear()
	send = bot.send_message(message.chat.id, "Мы всё настроили, теперь полетели ")

@bot.message_handler(commands=['find'])
def show_one(message):
	query_find_me = "SELECT id, name, city, info, image FROM forms WHERE id != %s ORDER BY RAND() LIMIT 1" % message.chat.id
	tgbot.execute(query_find_me)
	result = tgbot.fetchall()
	if len(result) != 0:
		row = result[0]
		bot.send_message(message.chat.id, row[1] + " из " + row[2])
		bot.send_message(message.chat.id, row[3])
		bot.send_photo(message.chat.id, row[4])
		send = bot.send_message(message.chat.id, "Напиши like или dislike")
		bot.register_next_step_handler(send, get_vote, row[0])
	else:
		bot.send_message(message.chat.id, "нет анкеты")

def get_vote(message, id):
	if message.text == 'like':
		send = bot.send_message(message.chat.id, "Ok: %s" % id)
		query_find_me = "SELECT id, name, city, info, image FROM forms WHERE id == %s ORDER BY RAND() LIMIT 1" % message.chat.id
		tgbot.execute(query_find_me)
		result = tgbot.fetchall()
		send = bot.send_message(id, "Тобой заинтересовались:")
		if len(result) == 0:
			bot.send_message(id, "нет анкеты")
		else:
			row = result[0]
			bot.send_message(id, row[0] + " из " + row[1])
			bot.send_message(id, row[2])
			bot.send_photo(id, row[3])
		bot.send_message(id, "like или dislike?")
		bot.register_next_step_handler(send, get_match, message.chat.id, message.from_user.username)
	elif message.text == 'dislike':
		send = bot.send_message(message.chat.id, "Not Ok: %s" % id)
	else:
		send = bot.send_message(message.chat.id, "Напиши like или dislike")
		bot.register_next_step_handler(send, get_vote, id)

def get_match(message, id, username_second):
	if message.text == 'like':
		bot.send_message(id, "Хватай его - t.me/%s!" % message.from_user.username)
		bot.send_message(message.chat.id, "У вас взаимность! t.me/%s" % username_second)
	elif message.text != 'dislike':
		send = bot.send_message(message.chat.id, "like или dislike")
		bot.register_next_step_handler(send, get_vote, id, username_second)

@bot.message_handler(commands=['me'])
def show_one(message):
	query_find_me = "SELECT name, city, info, image FROM forms WHERE id = %s" % message.chat.id
	tgbot.execute(query_find_me)
	result = tgbot.fetchall()
	bot.send_message(message.chat.id, "Вот твоя анкета:")
	if len(result) == 0:
		bot.send_message(message.chat.id, "bruh")
	else:
		row = result[0]
		bot.send_message(message.chat.id, row[0] + " из " + row[1])
		bot.send_message(message.chat.id, row[2])
		bot.send_photo(message.chat.id, row[3])
	bot.send_message(message.chat.id, message.chat.id)
	bot.send_message(message.chat.id, message.from_user.username)


bot.polling()
