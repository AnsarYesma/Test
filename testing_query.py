# from db import run as sql
import db

query_add_user = """
INSERT users(id) VALUES (%s);
"""

query_add_rate = """
INSERT rates(id_subject, id_object) VALUES (%s, %s);
"""

for id in range(1, 50):
    x = [id]
    db.tgbot.execute(query_add_user, x)
db.connection.commit()

for id in range(1, 50):
    for id1 in range(1, 50):
        if id != id1:
            x = [id, id1]
            db.tgbot.execute(query_add_rate, x)
	
db.connection.commit()