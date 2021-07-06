from getpass import getpass
from mysql.connector import connect, Error

connection = connect(
    host="TabuBot.mysql.pythonanywhere-services.com",
    user="TabuBot",
    password="AnsarAskar123",
    database="tgbot"
)

tgbot = connection.cursor()
def get_sql(query):
    tgbot.execute(query)
    result = tgbot.fetchall()
    if len(result) == 0:
        result = None
    return result

def getone_sql(query):
    tgbot.execute(query)
    result = tgbot.fetchone()
    return result

def execute_sql(query):
    tgbot.execute(query)
    connection.commit()

def execute_many(query, data):
    tgbot.execute_many(query, data)
    connection.commit()


'''
CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(100),
    registration_date DATE,
    last_active DATE
);

CREATE TABLE list (
    id INT,
    id_object INT,
    PRIMARY KEY (id, id_object),
    FOREIGN KEY (id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (id_object) REFERENCES users(id) ON DELETE CASCADE
);


CREATE TABLE forms (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    year YEAR(4),
    gender VARCHAR(100),
    city VARCHAR(100),
    info VARCHAR(10000),
    image LONGBLOB,
    isActive BOOl,
    lastActive DATE,
    popularity INT,
    FOREIGN KEY (id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE rates (
    id INT,
    id_object INT,
    text_message VARCHAR(100),
    PRIMARY KEY (id, id_object),
    FOREIGN KEY (id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (id_object) REFERENCES users (id) ON DELETE CASCADE
);
'''
