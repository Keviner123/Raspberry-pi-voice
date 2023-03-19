
# from Controller.Webserver import Webserver
from View.hotword_listener import HotwordDetector
from DAL.SoundFilePlayer import SoundFilePlayer

# WebserverController = Webserver(80)
soundfileplayer = SoundFilePlayer()


if __name__ == '__main__':
    hotwordetector = HotwordDetector("KqwUDxJhP+vf3BYnrH3/VXb5Uy2qOr50MhrMCflhbybizGB15keeeA==")

    while hotwordetector.wait_for_hotwords():
        print("hej")
        soundfileplayer.PlayMp3("assets/ding.mp3")
