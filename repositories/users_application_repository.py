import psycopg2
from psycopg2 import sql

conn = psycopg2.connect(
    dbname="voice-assistant",
    user="postgres",
    password="qwerty007",
    host="localhost",
    port="5432"
)
users_application_table = "users_application"


class UsersApplicationRepository:
    def is_user_application_exists(self, user_id, application_id):
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("SELECT * FROM {} WHERE user_id = %s and application_id = %s").format(
                    sql.Identifier(users_application_table)),
                (user_id, application_id))
            return cursor.fetchone()

    def save_into_users_application(self, user_id, application_id):
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("INSERT INTO {} (user_id, application_id) VALUES (%s, %s)")
                .format(sql.Identifier(users_application_table)), (user_id, application_id))
        conn.commit()
