from getpass import getpass
from mysql.connector import connect, Error

create_users_query = """
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    year YEAR(4),
    gender VARCHAR(100),
    city VARCHAR(100),
    info VARCHAR(max),
    image LONGBLOB
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
