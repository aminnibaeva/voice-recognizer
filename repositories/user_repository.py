import psycopg2
from psycopg2 import sql

conn = psycopg2.connect(
    dbname="voice-assistant",
    user="postgres",
    password="qwerty007",
    host="localhost",
    port="5432"
)
users_table = "users"


class UsersRepository:
    def get_user_id_by_username(self, username):
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("SELECT id FROM {} WHERE username = %s").format(sql.Identifier(users_table)),
                (username,))
            return cursor.fetchone()
