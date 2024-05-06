import pickle
from itertools import product

import nltk
import spacy
from keras import Sequential
from keras.layers import Dense, Dropout
from nltk.corpus import wordnet
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder

from repositories.page_repository import PageRepository
from repositories.trained_models_repository import TrainedModelsRepository
from services.traslation_service import TranslatorService

page_repository = PageRepository()
trained_models_repository = TrainedModelsRepository()
translator_service = TranslatorService()
nltk.download('wordnet')
nlp = spacy.load("ru_core_news_sm")


class ModelService:
    def train_model(self, application_id):
        search_words = ["Go to the ", "Navigate to the ", "Return to the ", "Click on the ", "Take me back to the ",
                        "Open the ", "Access the ", "Direct me to the ", "Visit the ", "Bring me to the ", "Load the ",
                        "Show up "]

        rows = page_repository.get_page_associations_by_application_id(application_id)
        page_names = []
        associations = []

        for row in rows:
            translated_associations = translator_service.translate(row[3], 'en')
            for association in translated_associations.text.split(","):
                # for search_word in search_words:
                #     page_names.append(row[2])
                #     associations.append(search_word + association)
                synonyms = find_phrase_synonyms(association)
                synonyms.append(association)
                for search_word in search_words:
                    for synonym in synonyms:
                        page_names.append(row[2])
                        associations.append(search_word + " " + synonym)

        # Векторизация текста запросов
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(associations)

        # Кодирование меток классов (категории предметов поиска)
        label_encoder = LabelEncoder()
        y_categories = label_encoder.fit_transform(page_names)

        # Создание нейронной сети для классификации запросов
        model_categories = Sequential([
            Dense(128, input_shape=(X.shape[1],), activation='relu'),
            Dropout(0.5),
            Dense(64, activation='relu'),
            Dropout(0.5),
            Dense(len(label_encoder.classes_), activation='softmax')
        ])

        # Компиляция модели
        model_categories.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        # Обучение модели
        model_categories.fit(X.toarray(), y_categories, epochs=10, batch_size=32)

        serialized_model = pickle.dumps(model_categories)
        save_vectorizer = pickle.dumps(vectorizer)
        save_label_encoder = pickle.dumps(label_encoder)

        is_model_exists = trained_models_repository.is_trained_model_exists_by_application_id(application_id)

        if is_model_exists:
            trained_models_repository.update_trained_models(serialized_model, save_vectorizer, save_label_encoder,
                                                            application_id)
        else:
            trained_models_repository.save_trained_models(serialized_model, save_vectorizer, save_label_encoder,
                                                          application_id)


def find_phrase_synonyms(phrase):
    phrase_synonyms = []
    words = phrase.split()
    for word in words:
        word_synonyms = set()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                word_synonyms.add(lemma.name())
        phrase_synonyms.append(word_synonyms)
    phrase_combinations = product(*phrase_synonyms)
    return [' '.join(combination) for combination in phrase_combinations]
