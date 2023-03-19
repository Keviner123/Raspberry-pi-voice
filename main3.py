
# from Controller.Webserver import Webserver
# WebserverController = Webserver(80)

from View.hotword_listener import HotwordDetector
from View.voice_listener import VoiceListener
from DAL.sound_file_player import SoundFilePlayer



if __name__ == '__main__':
    hotwordetector = HotwordDetector("KqwUDxJhP+vf3BYnrH3/VXb5Uy2qOr50MhrMCflhbybizGB15keeeA==")
    soundfileplayer = SoundFilePlayer()
    voicelistener = VoiceListener()

    while hotwordetector.wait_for_hotwords():
        soundfileplayer.play_mp3_async("assets/ding.mp3")

        voicelistener.start_recording()
        print("done recording")
