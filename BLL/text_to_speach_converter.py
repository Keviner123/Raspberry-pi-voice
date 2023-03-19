from gtts import gTTS

class TextToSpeechConverter:
    def __init__(self) -> None:
        pass

    def convert_text_to_mp3(self, text: str):
        mp3builder = gTTS(text = text, lang='da', slow=True)
        mp3builder.save("output.mp3")