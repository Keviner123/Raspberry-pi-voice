
from Controller.SoundFilePlayer import SoundFilePlayer
from Controller.Webserver import Webserver
from Controller.VoiceActivation import VoiceActivation


SoundFilePlayerController = SoundFilePlayer()
WebserverController = Webserver(80)
VoiceActivationController = VoiceActivation()


VoiceActivationController.StartListening()
