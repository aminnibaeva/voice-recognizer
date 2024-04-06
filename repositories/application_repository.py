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

    def get_language_by_token(self, token):
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL(
                    "SELECT language FROM {} LEFT JOIN {} ON application.language_id = language_codes.id WHERE token = %s")
                .format(sql.Identifier(language_codes, application_table)),
                (token,))
            return cursor.fetchone()
