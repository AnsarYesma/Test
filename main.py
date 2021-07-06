import telebot
from db import *
import urllib
import os
import json
from botData import token
from botImage import get_blob

bot = telebot.TeleBot(token)

# DEBUG PART
# @bot.message_handler(commands=['debug'])
# def starting(message):
# 	global user
# 	user = []
# 	curr_id = int(input("ID_debug: "))
# 	user.append(curr_id)
# 	query_checkFirst = """
# 	SELECT id FROM tgbot.users WHERE id = %s
# 	""" % curr_id
# 	tgbot.execute(query_checkFirst)
# 	res = tgbot.fetchall()
# 	if len(res) == 0:
# 		bot.send_message(message.chat.id, "Привет студент! Как подготовка? Если ты хочешь найти единомышленников, давай познакомимся !")
# 	else:
# 		bot.send_message(message.chat.id, "Привет студент! Хочешь поменять анкету? Для отмены можешь отправить 'Отмена' на любом вопросе.")
# 	send = bot.send_message(message.chat.id, "Как мне тебя звать ?")
# 	bot.register_next_step_handler(send, get_name)


#Создание анкеты

execute_sql("USE TabuBot$tgbot;")

@bot.message_handler(commands=['start'])
def starting(message):
	global user
	user = []
	curr_id = message.chat.id
	user.append(curr_id)
	query = "SELECT id FROM users WHERE id = %s" % curr_id
	res = get_sql(query)
	if res == None:
		bot.send_message(message.chat.id, "Привет студент! Как подготовка? Если ты хочешь найти единомышленников, давай познакомимся !")
	else:
		bot.send_message(message.chat.id, "Привет студент! Хочешь поменять анкету? Для отмены можешь отправить 'Отмена' на любом вопросе.")
	send = bot.send_message(message.chat.id, "Как мне тебя звать ?")
	bot.register_next_step_handler(send, get_name)

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
	query_add_user = "REPLACE INTO users(id, username) VALUES (%s, %s)"
	query_add_form = "REPLACE INTO forms(id, name, city, info, image) VALUES (%s, %s, %s, %s, %s)"
	# id name city info photo
	temp = [user[0], message.from_user.username]
	tgbot.execute(query_add_user, temp)
	tgbot.execute(query_add_form, user)
	add_to_list(user[0])
	connection.commit()
	user.clear()
	send = bot.send_message(message.chat.id, "Мы всё настроили, теперь полетели ")

def add_to_list(id):
	query = "SELECT id FROM users WHERE id != %s" % id
	result = get_sql(query)
	if result == None:
		return
	query = "INSERT list(id, id_object) VALUES(%s, %s)"
	for x in result:
		execute_sql(query % (x[0], id))

def refresh(id):
	query = "SELECT id FROM users WHERE id != %s" % id
	result = get_sql(query)
	if result == None:
		return False
	query = "INSERT list(id, id_object) VALUES(%s, %s)"
	for x in result:
		execute_sql(query % (id, x[0]))
	return True


#Поиск анкет
@bot.message_handler(commands=['find'])
def show_one(message):
	id = message.chat.id
	query = "SELECT id_object FROM list WHERE id = %s ORDER BY RAND() LIMIT 1" % message.chat.id
	id_obj = getone_sql(query)
	if (id_obj == None):
		if not refresh(id):
			bot.send_message(id, "Нет людей! Попробуйте позже!")
			return
		else:
			id_obj = get_sql(query)
	id_obj = id_obj[0]
	print(id, id_obj)
	query = "DELETE FROM list WHERE id = %s AND id_object = %s" % (message.chat.id, id_obj)
	execute_sql(query)
	query = "SELECT id, name, city, info, image FROM forms WHERE id = %s" % id_obj
	result = getone_sql(query)
	if result != None:
		bot.send_message(id, result[1] + " из " + result[2])
		bot.send_message(id, result[3])
		bot.send_photo(id, result[4])
		send = bot.send_message(id, "Напиши like или dislike")
		bot.register_next_step_handler(send, get_vote, result[0])
	else:
		bot.send_message(id, "Анкета не найдена, ошибка")

#Деактивация анкеты
# @bot.message_handler(commands=['deactivate'])
# def show_one(message):
#

def get_vote(message, id):
	if message.text == 'like':
		# debug_send = bot.send_message(message.chat.id, "Ok: %s" % id)
		query = "REPLACE INTO rates(id, id_object) VALUES(%s, %s)" % (id, message.chat.id)
		execute_sql(query)
		send = bot.send_message(id, "Тобой заинтересовались! Напиши команду /interest, чтобы увидеть, кто это был")
	elif message.text != 'dislike':
		send = bot.send_message(message.chat.id, "Напиши like или dislike")
		bot.register_next_step_handler(send, get_vote, id)

@bot.message_handler(commands=['interest'])
def show_interest(message):
	query = "SELECT id_object FROM rates WHERE id = %s ORDER BY id_object LIMIT 1" % message.chat.id
	obj_id = get_sql(query)[0][0]
	query = "DELETE FROM rates WHERE id_object = %s AND id = %s" % (obj_id, message.chat.id)
	execute_sql(query)
	query = "SELECT name, city, info, image FROM forms WHERE id = %s" % obj_id
	result = get_sql(query)
	if result == None:
		bot.send_message(message.chat.id, "На этом всё. Напиши /find для поиска анкет")
	else:
		row = result[0]
		bot.send_message(message.chat.id, row[0] + " из " + row[1])
		bot.send_message(message.chat.id, row[2])
		bot.send_photo(message.chat.id, row[3])
	send = bot.send_message(message.chat.id, "like или dislike?")
	bot.register_next_step_handler(send, get_match, obj_id, show_interest)

def get_match(message, id, function):
	if message.text == 'like':
		query = "SELECT username FROM users WHERE id = %s" % id
		res = getone_sql(query)[0]
		bot.send_message(id, "Хватай его - t.me/%s!" % message.from_user.username)
		bot.send_message(message.chat.id, "У вас взаимность! t.me/%s" % res)
	elif message.text != 'dislike':
		send = bot.send_message(message.chat.id, "like или dislike")
		bot.register_next_step_handler(send, get_match, id, function)
	function()


@bot.message_handler(commands=['me'])
def show_one(message):
	query_find_me = "SELECT name, city, info, image FROM forms WHERE id = %s" % message.chat.id
	tgbot.execute(query_find_me)
	result = tgbot.fetchall()
	bot.send_message(message.chat.id, "Вот твоя анкета:")
	if result == None:
		bot.send_message(message.chat.id, "Error")
	else:
		row = result[0]
		bot.send_message(message.chat.id, row[0] + " из " + row[1])
		bot.send_message(message.chat.id, row[2])
		bot.send_photo(message.chat.id, row[3])
	bot.send_message(message.chat.id, message.chat.id)
	bot.send_message(message.chat.id, message.from_user.username)


bot.polling()
print("OK")
