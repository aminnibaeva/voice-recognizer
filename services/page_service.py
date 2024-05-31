import pickle

import numpy as np

from repositories.trained_models_repository import TrainedModelsRepository

trained_models_repository = TrainedModelsRepository()

class PageService:
    def get_page_name(self, application_id, text):
        loaded_model_serialized = trained_models_repository.get_serialized_model_by_application_id(application_id)

        loaded_model = pickle.loads(loaded_model_serialized['model'])
        vectorizer = pickle.loads(loaded_model_serialized['vectorizer'])
        label_encoder = pickle.loads(loaded_model_serialized['label_encoder'])

        query_vec = vectorizer.transform([text])
        category_prediction = np.argmax(loaded_model.predict(query_vec))
        page_name = label_encoder.inverse_transform([category_prediction])[0]

        return page_name
