
from Controller.SoundFilePlayer import SoundFilePlayer
from Controller.Webserver import Webserver

SoundFilePlayerController = SoundFilePlayer()

WebserverController = Webserver(80)

# SoundFilePlayerController.PlayMp3("sound.mp3")
WebserverController.start_webserver()

