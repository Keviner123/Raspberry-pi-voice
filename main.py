import asyncio
import time
import yaml
import subprocess

import board
import neopixel

from BLL.accesspoint import Accesspoint
from BLL.internet_checker import InternetChecker
from BLL.question_answering_service import QuestionAnsweringService
from BLL.sound_file_player import SoundFilePlayer
from BLL.text_to_speach_converter import TextToSpeechConverter
from BLL.webserver import Webserver

from View.hotword_listener import HotwordDetector
from View.voice_listener import VoiceListener


async def main():
    with open("config.yaml", "r", encoding="utf-8") as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader)

    # pixels = neopixel.NeoPixel(board.D18, 60)

    hotwordetector = HotwordDetector(config["picovoice-apikey"])
    soundfileplayer = SoundFilePlayer()
    voicelistener = VoiceListener()
    texttospeechconverter = TextToSpeechConverter()
    questionansweringservice = QuestionAnsweringService("wss://api.prøve.svendeprøven.dk/ws/r2d2device", "00:B0:D0:63:C2:11")
    internetchecker = InternetChecker()


  


    while hotwordetector.wait_for_hotwords():
        if(internetchecker.check()):


            if(questionansweringservice.token == None):
                subprocess.run(['espeak', '-v', 'en', "No token has been set, please add me in the dashboard"])
                response = await questionansweringservice.authenticate()
                subprocess.run(['espeak', '-v', 'en', "Thank you"])






            soundfileplayer.play_mp3_async(config["activation-sound"])
            
            time.sleep(1)


            voicelistener.start_recording()

            try:
                transcribe_text = voicelistener.transcribe()
                print(transcribe_text)

                question_answer = questionansweringservice.get_answer(transcribe_text)
                
                texttospeechconverter.convert_text_to_mp3(question_answer)
                soundfileplayer.play_mp3("output.mp3")


            except IndexError:
                print("No voice detected")
        else:
            print("Creating AP")
            subprocess.run(['espeak', '-v', 'en', "I was unable to connect to the internet, starting wifi hotspot."])

            accesspoint = Accesspoint("R2D2-Config", "passwword")
            accesspoint.start()
            
            time.sleep(5)
            
            webserver = Webserver()
            webserver.start()

asyncio.run(main())