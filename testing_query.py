# from db import run as sql
import db

query_add_user = """
INSERT users(id) VALUES (%s);
"""

query_add_forms = """
INSERT forms(id, name, city, info, image) VALUES (%s, %s, %s, %s, %s);
"""

def convert_to_blob(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data

morgen = convert_to_blob("example.jpg")

for id in range(1, 50):
    x = [id]
    db.tgbot.execute(query_add_user, x)
    x = [id, "НиктоТест%s" % id, "Алматы", "Я не напишу симфонию, я искусственный", morgen]
    db.tgbot.execute(query_add_forms, x)

db.connection.commit()
#
# for id in range(1, 50):
#     for id1 in range(1, 50):
#         if id != id1:
#             x = [id, id1]
#             db.tgbot.execute(query_add_rate, x)

# db.connection.commit()
