import telebot
import db
from db import tgbot

def start_session (user_id):
    query = """
    SELECT id FROM users;
    """
    tgbot.execute(query)
    res = tgbot.fetchall()
    for x in res:
        print(x[0], "\n")

start_session(1)