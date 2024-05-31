from pymongo import MongoClient

host = "localhost"
port = "27017"
dbname = "models"

mongo_uri = f"mongodb://{host}:{port}/{dbname}"

client = MongoClient(mongo_uri)

db = client[dbname]

collection = db["models"]


class TrainedModelsRepository:
    def save_trained_models(self, serialized_model, save_vectorizer, save_label_encoder, application_id):
        document = {
            "model": serialized_model,
            "vectorizer": save_vectorizer,
            "label_encoder": save_label_encoder,
            "application_id": application_id
        }
        collection.update_one({"application_id": application_id}, {"$set": document}, upsert=True)

    def get_serialized_model_by_application_id(self, application_id):
        document = collection.find_one({"application_id": application_id})
        return document
