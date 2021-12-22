# for PostgreSQL
host = "127.0.0.1"
user = "filebot"
password = "filebot"
db_name = "file_hosting"
port = 5432

import psycopg2
bot_username = ''
TOKEN = ''

def select_all():
    global bot_username, TOKEN
    db = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    cursor = db.cursor()
    cursor.execute(
            """SELECT value FROM settings WHERE name = 'token' ORDER BY id ASC;""")
    TOKEN = cursor.fetchall()
    TOKEN = TOKEN[0][0]
    cursor = db.cursor()
    cursor.execute(
            """SELECT value FROM settings WHERE name = 'username' ORDER BY id ASC;""")
    bot_username = cursor.fetchall()
    bot_username = bot_username[0][0]

select_all()