import psycopg2
from psycopg2 import sql

conn = psycopg2.connect(
    dbname="voice-assistant",
    user="postgres",
    password="qwerty007",
    host="localhost",
    port="5432"
)

trained_models_table_name = "trained_models"


class TrainedModelsRepository:
    def is_trained_model_exists_by_application_id(self, application_id):
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("SELECT 1 FROM {} WHERE application_id = %s").format(sql.Identifier(trained_models_table_name)),
                (application_id,))
            return cursor.fetchone() is None

    def get_serialized_model(self, application_id):
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("SELECT model FROM {} WHERE application_id = %s").format(
                    sql.Identifier(trained_models_table_name)),
                (application_id,))
            return cursor.fetchone()[0]

    def insert_into_trained_models(self, serialized_model, application_id):
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("INSERT INTO {} (model, application_id) VALUES (%s, %s)")
                .format(sql.Identifier(trained_models_table_name)), (serialized_model, application_id))
        conn.commit()

    def update_trained_models(self, serialized_model, application_id):
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("UPDATE {} SET model = %s WHERE application_id = %s")
                .format(sql.Identifier(trained_models_table_name)),
                (serialized_model, application_id))
        conn.commit()
