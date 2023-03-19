import io
import os
from google.cloud import speech

class GoogleSpeechToTextClient:
    def __init__(self, credentials_path):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
        self.client = speech.SpeechClient()

    def transcribe_audio_file(self, file_path:str) -> str:

        #the path of your audio file
        file_name = file_path
        with io.open(file_name, "rb") as audio_file:
            content = audio_file.read()
            audio = speech.RecognitionAudio(content=content)


        config = speech.RecognitionConfig(
            encoding = 'LINEAR16',
            language_code = 'da-DK',
            audio_channel_count = 1,
        )

        # Sends the request to google to transcribe the audio
        response = self.client.recognize(request={"config": config, "audio": audio})
        return(response.results[0].alternatives[0].transcript)
