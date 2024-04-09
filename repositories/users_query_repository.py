import psycopg2
from psycopg2 import sql

conn = psycopg2.connect(
    dbname="voice-assistant",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
users_query_table = "users_query"


class UsersQueryRepository:
    def save_user_query(self, application_id, user_id, query):
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("INSERT INTO {} (user_id, query, application_id) VALUES (%s, %s, %s)").format(
                    sql.Identifier(users_query_table)),
                (user_id, query, application_id))
        conn.commit()

    def is_user_query_exists(self, user_id, query):
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("SELECT 1 FROM {} WHERE user_id = %s and query = %s").format(sql.Identifier(users_query_table)),
                (user_id, query))
            return cursor.fetchall()

    def update_user_query_by_user_id_and_query(self, application_id, user_id, query):
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("UPDATE {} SET number_of_visits = (number_of_visits + 1) WHERE user_id = %s and query = %s and application_id = %s")
                .format(sql.Identifier(users_query_table)),
                (user_id, query, application_id))
        conn.commit()

    def update_user_query_by_user_query_id(self, user_query_id):
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("UPDATE {} SET number_of_visits = (number_of_visits + 1) WHERE user_query_id = %s ")
                .format(sql.Identifier(users_query_table)), user_query_id)
        conn.commit()

    def delete_user_query_by_user_query_id(self, user_query_id):
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("DELETE FROM {} WHERE user_query_id = " + user_query_id)
                .format(sql.Identifier(users_query_table)))
        conn.commit()
