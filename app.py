from flask import Flask
from flask_cors import CORS

from controllers.model_controller import model_bp as model_bp
from controllers.voice_recognize_controller import voice_recognize_bp as voice_recognize_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(model_bp)
app.register_blueprint(voice_recognize_bp)

if __name__ == '__main__':
    app.run(debug=True)
