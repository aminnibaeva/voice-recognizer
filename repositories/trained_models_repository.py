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
application_table_name = "application"


class TrainedModelsRepository:
    def is_trained_model_exists_by_application_id(self, application_id):
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("SELECT 1 FROM {} WHERE application_id = %s")
                .format(sql.Identifier(trained_models_table_name)), (application_id,))
            return cursor.fetchone() is not None

    def get_serialized_model_by_token(self, token):
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL(
                    "SELECT model FROM {} LEFT JOIN {} ON trained_models.application_id = application.application_id "
                    "WHERE token = %s")
                .format(sql.Identifier(trained_models_table_name), sql.Identifier(application_table_name)),
                (token,))
            return cursor.fetchone()[0]

    def get_serialized_model_by_application_id(self, application_id):
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL(
                    "SELECT model, vectorizer, label_encoder FROM {} WHERE application_id = %s")
                .format(sql.Identifier(trained_models_table_name)),
                (application_id,))
            return cursor.fetchone()

    def save_trained_models(self, serialized_model, save_vectorizer, save_label_encoder, application_id):
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("INSERT INTO {} (model, vectorizer, label_encoder, application_id) VALUES (%s, %s, %s, %s)")
                .format(sql.Identifier(trained_models_table_name)),
                (serialized_model, save_vectorizer, save_label_encoder, application_id))
        conn.commit()

    def update_trained_models(self, serialized_model, save_vectorizer, save_label_encoder, application_id):
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("UPDATE {} SET model = %s, vectorizer = %s, label_encoder = %s WHERE application_id = %s")
                .format(sql.Identifier(trained_models_table_name)),
                (serialized_model, save_vectorizer, save_label_encoder, application_id))
        conn.commit()
