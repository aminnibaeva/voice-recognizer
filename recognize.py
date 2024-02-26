from io import BytesIO

import speech_recognition as sr
from flask import Flask, request
from pydub import AudioSegment

app = Flask(__name__)
recognizer = sr.Recognizer()


@app.route('/recognize', methods=['POST'])
def read_document():
    data = request.data
    audio = AudioSegment.from_file(BytesIO(bytearray(data)))
    wav_data = audio.export(format="wav")

    with sr.AudioFile(wav_data) as source:
        audio_data = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio_data, language="ru-RU")
        except sr.UnknownValueError:
            return ""


if __name__ == '__main__':
    app.run(debug=True)
