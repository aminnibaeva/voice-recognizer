import speech_recognition as sr
from pydub import AudioSegment

recognizer = sr.Recognizer()


class RecognizerService:
    def recognize_audio(self, data, language):
        audio = AudioSegment.from_file(data)
        wav_data = audio.export(format="wav")

        with sr.AudioFile(wav_data) as source:
            audio_data = recognizer.record(source)
            try:
                return recognizer.recognize_google(audio_data, language=language)
            except sr.UnknownValueError:
                return ""
