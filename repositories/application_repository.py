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
language_codes = "language_codes"


class ApplicationRepository:
    def get_application_id_by_token(self, token):
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("SELECT application_id FROM {} WHERE token = %s").format(sql.Identifier(application_table)),
                (token,))
            return cursor.fetchone()

    def get_language_by_application_id(self, application_id):
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL(
                    "SELECT code FROM {} WHERE application_id = %s")
                .format(sql.Identifier(application_table)),
                (application_id,))
            return cursor.fetchone()
