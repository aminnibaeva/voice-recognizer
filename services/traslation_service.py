from googletrans import Translator

translator = Translator()


class TranslatorService:
    def translate(self, text, language):
        return translator.translate(text, dest=language)
