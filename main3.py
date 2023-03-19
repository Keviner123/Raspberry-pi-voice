
# from Controller.SoundFilePlayer import SoundFilePlayer
# from Controller.Webserver import Webserver
from View.hotword_detector import HotwordDetector


# WebserverController = Webserver(80)


if __name__ == '__main__':
    hotwordetector = HotwordDetector("assets/ding.mp3", "KqwUDxJhP+vf3BYnrH3/VXb5Uy2qOr50MhrMCflhbybizGB15keeeA==")

    while hotwordetector.wait_for_hotwords():
        print("hej")
