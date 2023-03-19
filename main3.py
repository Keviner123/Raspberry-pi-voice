import yaml

from BLL.text_to_speach_converter import TextToSpeechConverter
from View.hotword_listener import HotwordDetector
from View.voice_listener import VoiceListener
from DAL.sound_file_player import SoundFilePlayer



if __name__ == '__main__':

    with open("config.yaml", "r", encoding="utf-8") as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader)

    hotwordetector = HotwordDetector(config["picovoice-apikey"])
    soundfileplayer = SoundFilePlayer()
    voicelistener = VoiceListener()
    texttospeechconverter = TextToSpeechConverter()


    while hotwordetector.wait_for_hotwords():
        soundfileplayer.play_mp3_async(config["activation-sound"])

        voicelistener.start_recording()

        TranscribeText = voicelistener.transcribe()

        texttospeechconverter.convert_text_to_mp3(TranscribeText)

        soundfileplayer.play_mp3_async("output.mp3")