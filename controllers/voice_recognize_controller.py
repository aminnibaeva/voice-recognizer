from flask import request, Blueprint

from services.page_service import PageService
from services.recognizer_service import RecognizerService
from services.traslation_service import TranslatorService

voice_recognize_bp = Blueprint('voice_recognize', __name__)

recognizer_service = RecognizerService()
page_service = PageService()
translator_service = TranslatorService()


@voice_recognize_bp.route('/recognize/<int:applicationId>', methods=['POST'])
def recognize(applicationId):
    data = request.files['audio']

    query_text = recognizer_service.recognize_audio(data)
    translated_text = translator_service.translate(query_text, 'en')
    return page_service.get_page(applicationId, translated_text.text)
