import psycopg2
from psycopg2 import sql

conn = psycopg2.connect(
    dbname="voice-assistant",
    user="postgres",
    password="qwerty007",
    host="localhost",
    port="5432"
)
users_query_table = "users_query"


class UsersQueryRepository:
    def save_user_query(self, user_id, query):
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("INSERT INTO {} (user_id, query) VALUES (%s, %s)").format(
                    sql.Identifier(users_query_table)),
                (user_id, query))
        conn.commit()
