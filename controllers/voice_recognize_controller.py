from flask import request, Blueprint, json

from services.application_service import ApplicationService
from services.page_service import PageService
from services.recognizer_service import RecognizerService
from services.traslation_service import TranslatorService
from services.user_service import UserService

voice_recognize_bp = Blueprint('voice_recognize', __name__)

recognizer_service = RecognizerService()
page_service = PageService()
user_service = UserService()
application_service = ApplicationService()
translator_service = TranslatorService()


@voice_recognize_bp.route('/recognize', methods=['POST'])
def recognize():
    data = request.files['audio']
    application_id = request.form['applicationId']
    username = request.form['username']
    language = application_service.get_language_by_application_id(application_id)

    query_text = recognizer_service.recognize_audio(data, language[0])
    translated_text = translator_service.translate(query_text, 'en')
    result = page_service.get_page(application_id, translated_text.text)
    user_service.save_user_query(username, application_id, result)
    return json.dumps({'result': result})
