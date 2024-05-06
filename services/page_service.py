import pickle

import numpy as np

from repositories.trained_models_repository import TrainedModelsRepository

trained_models_repository = TrainedModelsRepository()

class PageService:
    def get_page(self, application_id, text):
        loaded_model_serialized = trained_models_repository.get_serialized_model_by_application_id(application_id)

        # Предсказание категории предмета поиска
        loaded_model = pickle.loads(loaded_model_serialized[0])
        vectorizer = pickle.loads(loaded_model_serialized[1])
        label_encoder = pickle.loads(loaded_model_serialized[2])

        query_vec = vectorizer.transform([text])
        # Предсказание категории предмета поиска
        category_prediction = np.argmax(loaded_model.predict(query_vec))
        result = label_encoder.inverse_transform([category_prediction])[0]

        return result
