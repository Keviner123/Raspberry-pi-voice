
from Controller.SoundFilePlayer import SoundFilePlayer
from Controller.Webserver import Webserver
from Controller.VoiceActivation import VoiceActivation


WebserverController = Webserver(80)

VoiceActivationController = VoiceActivation("assets/ding.mp3")

VoiceActivationController.StartListening()
