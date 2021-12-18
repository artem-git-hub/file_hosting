import psycopg2
from config import *

db = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name
)
cursor = db.cursor()


async def select_db(whatis="*", fromis="users", whereis=''):
    if whereis == "":
        cursor.execute("""SELECT {} FROM {} ORDER BY id ASC;""".format(whatis, fromis))
    else:
        # print("""SELECT {} FROM {} WHERE {};""".format(whatis, fromis, whereis))
        cursor.execute(
            """SELECT {} FROM {} WHERE {} ORDER BY id ASC;""".format(whatis, fromis, whereis))
    return cursor.fetchall()



async def insert_db(name_table, column, values):
    column = str(column).replace("'", "")
    # print(f"""-- INSERT INTO {name_table} {column} VALUES{values};""")
    cursor.execute(
        f"""INSERT INTO {name_table} {column} VALUES{values};"""
    )
    db.commit()


async def delete_db(name_table, where):
    # print(f"""-- DELETE FROM {name_table} WHERE {where};""")
    cursor.execute(
        f"""DELETE FROM {name_table} WHERE {where};""")
    db.commit()


async def update_db(name_table, column, value, whereis):
    # print(f"""UPDATE {name_table} SET {column} = {value} WHERE {whereis};""")
    cursor.execute(
        f"""UPDATE {name_table} SET {column} = {value} WHERE {whereis};""")
    db.commit()
