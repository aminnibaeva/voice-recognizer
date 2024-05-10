import numpy as np
import spacy
from keras import Sequential
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from keras.layers import Dense, Dropout

# Загрузка модели SpaCy для обработки текста
nlp = spacy.load("ru_core_news_sm")

# Обучающие данные
queries = [
    "цена от 100 до 1400 число колёс 5 наибольшая популярность максимальная размер с бренд сяоми",
    "число колёс 1 наименьшая цена от 500 до 600 размер м популярность максимальная бренд профи",
]
categories = ['цена', 'популярность', 'размер', 'бренд', 'тип', 'число колёс']

# Векторизация текста запросов
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(queries)

# Кодирование меток классов (категории предметов поиска)
label_encoder_categories = LabelEncoder()
y_categories = label_encoder_categories.fit_transform(categories)

# Создание нейронной сети для классификации запросов
loaded_model_serialized = Sequential([
    Dense(128, input_shape=(X.shape[1],), activation='relu'),
    Dropout(0.5),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(len(label_encoder_categories.classes_), activation='softmax')
])

# Компиляция модели
loaded_model_serialized.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Обучение модели
loaded_model_serialized.fit(X.toarray(), y_categories, epochs=10, batch_size=32)


# Функция для анализа запроса и выполнения соответствующего действия
def process_query(text):
    # Векторизация текста запроса
    query_vec = vectorizer.transform([text])
    # Предсказание категории предмета поиска
    category_prediction = np.argmax(loaded_model_serialized.predict(query_vec))
    result = label_encoder_categories.inverse_transform([category_prediction])[0]
    print("Ищем предмет:", result)


# Пример использования
query1 = "цвет зелёный число колёс 5 тип чемодан"
process_query(query1)
