from flask import request, Blueprint

from services.page_service import PageService
from services.recognizer_service import RecognizerService
from services.traslation_service import TranslatorService
from services.user_service import UserService

voice_recognize_bp = Blueprint('voice_recognize', __name__)

recognizer_service = RecognizerService()
page_service = PageService()
user_service = UserService()
translator_service = TranslatorService()


@voice_recognize_bp.route('/recognize', methods=['POST'])
def recognize():
    data = request.files['audio']
    token = request.form['token']
    username = request.form['username']
    language = request.form['language']

    query_text = recognizer_service.recognize_audio(data, language)
    translated_text = translator_service.translate(query_text, 'en')
    result = page_service.get_page(token, translated_text.text)
    user_service.save_user_query(username, token, result)
    return result
