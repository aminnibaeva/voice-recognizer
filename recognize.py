import pickle
from io import BytesIO

import psycopg2
import speech_recognition as sr
from flask import Flask, request
from psycopg2 import sql
from pydub import AudioSegment
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

app = Flask(__name__)
recognizer = sr.Recognizer()

conn = psycopg2.connect(
    dbname="voice-assistant",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)


@app.route('/recognize', methods=['POST'])
def recognize():
    data = request.data
    audio = AudioSegment.from_file(BytesIO(bytearray(data)))
    wav_data = audio.export(format="wav")

    with sr.AudioFile(wav_data) as source:
        audio_data = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio_data, language="ru-RU")
        except sr.UnknownValueError:
            return ""


@app.route('/train-model', methods=['POST'])
def train_model():
    data = request.json

    application_id = data.get('application_id')

    page_table = "page"
    with conn.cursor() as cursor:
        cursor.execute(
            sql.SQL("SELECT * FROM {} WHERE application_id = %s").format(sql.Identifier(page_table)), (application_id,))

        search_words = ["перейти ", "перейти в", "открыть ", "открой ", "перейди ", "перейди в ", "покажи ",
                        "загрузить ", "загрузи ",
                        "просмотреть ", "посмотреть " "домашняя страница ", "главная страница ", "домой "]
        rows = cursor.fetchall()
        page_names = []
        associations = []
        for row in rows:
            for association in row[3].split(","):
                for search_word in search_words:
                    page_names.append(row[2])
                    associations.append(search_word + association)
        len(rows)

        X_train, X_test, y_train, y_test = train_test_split(associations, page_names, test_size=0.2, random_state=42)

        # Create a pipeline for text classification
        text_clf = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', LogisticRegression())
        ])

        # Train the model
        text_clf.fit(X_train, y_train)

        # Serialize the model to a binary format
        serialized_model = pickle.dumps(text_clf)

        # Insert the serialized model into the database
        model_table_name = "trained_models"
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("INSERT INTO {} (model, application_id) VALUES (%s, %s)").format(
                    sql.Identifier(model_table_name)), (serialized_model, application_id))
            conn.commit()

        return 'Model trained successfully'


@app.route('/get-page', methods=['POST'])
def get_page():
    data = request.json

    application_id = data.get('application_id')

    trained_models_table = "trained_models"
    with conn.cursor() as cursor:
        cursor.execute(
            sql.SQL("SELECT * FROM {} WHERE application_id = %s").format(sql.Identifier(trained_models_table)),
            (application_id,))
    loaded_model = cursor.fetchone()

    # Теперь вы можете использовать загруженную модель для предсказаний
    new_query = ["покаж дом страницу"]
    predicted_type_code = loaded_model.predict(new_query)
    print(f"Predicted Query Type Code: {predicted_type_code[0]}")


if __name__ == '__main__':
    app.run(debug=True)
