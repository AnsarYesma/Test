from getpass import getpass
from mysql.connector import connect, Error

users_table = """
CREATE TABLE users (
    id INT PRIMARY KEY,
    registration_date DATE,
    last_active DATE
)
"""

forms_table = """
CREATE TABLE forms (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    year YEAR(4),
    gender VARCHAR(100),
    city VARCHAR(100),
    info VARCHAR(max),
    image LONGBLOB,
    isActive BOOl,
    lastActive DATE,
    popularity INT,
    FOREIGN KEY (id) REFERENCES users (id) ON DELETE CASCADE
)
"""

rates_table = """
CREATE TABLE rates (
    id_subject INT,
    id_object INT,
    text_message VARCHAR(100),
    PRIMARY KEY (id_subject, id_object)
    FOREIGN KEY (id_subject) REFERENCES users (id_subject) ON DELETE CASCADE,
    FOREIGN KEY (id_object) REFERENCES users (id_object) ON DELETE CASCADE
)
"""

connection = connect(
    host="localhost",
    user="root",
    password="Ansar123@",
    database="tgbot"
)

# connc
tgbot = connection.cursor()

run = tgbot.execute



# show_table_query = connection.cursor

# with connection.cursor() as cursor:
#     cursor.execute(create_users_query)
#     # cursor.execute("DESCRIBE users")
#     cursor.execute("DESCRIBE users")
#     # Fetch rows from last executed query
#     result = cursor.fetchall()
#     for row in result:
#         print(row)


# print("GOOD")
