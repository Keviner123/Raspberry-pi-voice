import time
import yaml
import subprocess

from BLL.InternetChecker import InternetChecker
from BLL.question_answering_service import QuestionAnsweringService
from BLL.sound_file_player import SoundFilePlayer
from BLL.text_to_speach_converter import TextToSpeechConverter
from BLL.webserver import Webserver

from View.hotword_listener import HotwordDetector
from View.voice_listener import VoiceListener


if __name__ == '__main__':
    with open("config.yaml", "r", encoding="utf-8") as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader)

    hotwordetector = HotwordDetector(config["picovoice-apikey"])
    soundfileplayer = SoundFilePlayer()
    voicelistener = VoiceListener()
    texttospeechconverter = TextToSpeechConverter()
    questionansweringservice = QuestionAnsweringService()
    internetchecker = InternetChecker()

    while hotwordetector.wait_for_hotwords():

        if(internetchecker.check()):
            soundfileplayer.play_mp3_async(config["activation-sound"])
            
            time.sleep(1)

            voicelistener.start_recording()

            try:
                transcribe_text = voicelistener.transcribe()
                print(transcribe_text)

                question_answer = questionansweringservice.get_answer(transcribe_text)
                
                texttospeechconverter.convert_text_to_mp3(question_answer)
                soundfileplayer.play_mp3_async("output.mp3")


            except IndexError:
                print("No voice detected")
        else:
            print("Creating AP")
            create_ap_process = subprocess.Popen(["create_ap", "wlan0", "eth0", "R2D2-Config", "12345678", "--dhcp-dns", "192.168.4.1"])
            subprocess.run(['espeak', '-v', 'en', "I was unable to connect to the internet, starting wifi hotspot."])
            webserver = Webserver()
            webserver.start()