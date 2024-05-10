import psycopg2
from psycopg2 import sql

conn = psycopg2.connect(
    dbname="voice-assistant",
    user="postgres",
    password="qwerty007",
    host="localhost",
    port="5432"
)
filter_table = "filter"


class FilterRepository:
    def get_filter_names_by_application_id(self, application_id):
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("SELECT filter_name, filter_type FROM {} WHERE application_id = %s").format(sql.Identifier(filter_table)),
                (application_id,))
            return cursor.fetchall()
