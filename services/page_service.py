import pickle

from repositories.trained_models_repository import TrainedModelsRepository

trained_models_repository = TrainedModelsRepository()


class PageService:
    def get_page(self, application_id, text):
        loaded_model_serialized = trained_models_repository.get_serialized_model(application_id)

        loaded_model = pickle.loads(loaded_model_serialized)

        predicted_page = loaded_model.predict([text])

        return predicted_page[0]
