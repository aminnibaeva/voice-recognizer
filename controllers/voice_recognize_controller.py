from flask import request, Blueprint

from services.recognizer_service import RecognizerService

voice_recognize_bp = Blueprint('voice_recognize', __name__)

recognizer_service = RecognizerService()


@voice_recognize_bp.route('/recognize', methods=['POST'])
def recognize():
    data = request.data

    return recognizer_service.recognize_audio(data)
