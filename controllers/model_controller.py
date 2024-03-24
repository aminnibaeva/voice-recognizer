from flask import request, Blueprint

from services.model_service import ModelService

model_service = ModelService()
model_bp = Blueprint('model', __name__)


@model_bp.route('/train-model', methods=['POST'])
def train_model():
    data = request.json

    application_id = data.get('application_id')

    model_service.train_model(application_id)

    return 'Model trained successfully'
