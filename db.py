import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="stustop",            # або твій логін
        password="ilovepespatron",    # або твій пароль
        database="2read"       # назва БД
    )
