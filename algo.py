import telebot
import db

def start_session (user_id):
    query = """
    SELECT id FROM users
    """
    db.tgbot.execute()