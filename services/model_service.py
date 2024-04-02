import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from repositories.page_repository import PageRepository
from repositories.trained_models_repository import TrainedModelsRepository
from services.traslation_service import TranslatorService

page_repository = PageRepository()
trained_models_repository = TrainedModelsRepository()
translator_service = TranslatorService()


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
                for search_word in search_words:
                    page_names.append(row[2])
                    associations.append(search_word + association)

        X_train, X_test, y_train, y_test = train_test_split(associations, page_names, test_size=0.2, random_state=42)

        text_clf = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', LogisticRegression())
        ])

        text_clf.fit(X_train, y_train)

        serialized_model = pickle.dumps(text_clf)

        is_model_exists = trained_models_repository.is_trained_model_exists_by_application_id(application_id)

        if is_model_exists:
            trained_models_repository.update_trained_models(serialized_model, application_id)
        else:
            trained_models_repository.save_trained_models(serialized_model, application_id)
