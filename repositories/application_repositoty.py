import psycopg2
from psycopg2 import sql

conn = psycopg2.connect(
    dbname="voice-assistant",
    user="postgres",
    password="qwerty007",
    host="localhost",
    port="5432"
)
application_table = "application"


class ApplicationRepository:
    def get_application_id_by_token(self, token):
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("SELECT application_id FROM {} WHERE token = %s").format(sql.Identifier(application_table)),
                (token,))
            return cursor.fetchone()
