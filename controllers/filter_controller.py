from flask import request, Blueprint, json

from services.application_service import ApplicationService
from services.filter_service import FilterService
from services.recognizer_service import RecognizerService

filter_bp = Blueprint('filter', __name__)

filter_service = FilterService()
recognizer_service = RecognizerService()
application_service = ApplicationService()


@filter_bp.route('/get_filters', methods=['POST'])
def get_filters():
    data = request.files['audio']
    application_id = request.form['applicationId']
    language = application_service.get_language_by_application_id(application_id)

    query_text = recognizer_service.recognize_audio(data, language[0])
    result = filter_service.get_filters(application_id, query_text)
    print(result)
    return json.dumps({'result': result})
