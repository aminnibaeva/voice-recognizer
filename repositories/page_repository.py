import psycopg2
from psycopg2 import sql

conn = psycopg2.connect(
    dbname="voice-assistant",
    user="postgres",
    password="qwerty007",
    host="localhost",
    port="5432"
)
page_table = "page"


class PageRepository:
    def get_page_associations_by_application_id(self, application_id):
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("SELECT * FROM {} WHERE application_id = %s").format(sql.Identifier(page_table)),
                (application_id,))
            return cursor.fetchall()

    def get_page_url_by_application_id_and_page_name(self, application_id, page_name):
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("SELECT url FROM {} WHERE application_id = %s and page_name = %s").format(
                    sql.Identifier(page_table)),
                (application_id, page_name))
            return cursor.fetchone()
