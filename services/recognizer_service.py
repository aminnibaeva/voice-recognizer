from io import BytesIO

import speech_recognition as sr
from pydub import AudioSegment

recognizer = sr.Recognizer()


class RecognizerService:
    def recognize_audio(self, data):
        audio = AudioSegment.from_file(BytesIO(bytearray(data)))
        wav_data = audio.export(format="wav")

        with sr.AudioFile(wav_data) as source:
            audio_data = recognizer.record(source)
            try:
                return recognizer.recognize_google(audio_data, language="ru-RU")
            except sr.UnknownValueError:
                return ""
