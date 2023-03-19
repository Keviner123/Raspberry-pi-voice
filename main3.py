
# from Controller.Webserver import Webserver
# WebserverController = Webserver(80)

from View.hotword_listener import HotwordDetector
from DAL.SoundFilePlayer import SoundFilePlayer

soundfileplayer = SoundFilePlayer()


if __name__ == '__main__':
    hotwordetector = HotwordDetector("KqwUDxJhP+vf3BYnrH3/VXb5Uy2qOr50MhrMCflhbybizGB15keeeA==")

    while hotwordetector.wait_for_hotwords():
        print("hej")
        soundfileplayer.play_mp3("assets/ding.mp3")
