from BLL.google_speech_to_text_client import GoogleSpeechToTextClient

gstc = GoogleSpeechToTextClient("login.json")

print(gstc.transcribe_audio_file("test.wav"))