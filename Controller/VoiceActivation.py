import pvporcupine
import pyaudio
import struct

from Controller.SoundFilePlayer import SoundFilePlayer

class VoiceActivation:
    def __init__(self, activationSound) -> None:
        self.SoundFilePlayerController = SoundFilePlayer()
        self.activationSound = activationSound

        self.SoundFilePlayerController.PlayMp3(activationSound)

        pass
    
    def StartListening(self):

        porcupine = None
        pa = None
        audio_stream = None

        try:
            access_key = "KqwUDxJhP+vf3BYnrH3/VXb5Uy2qOr50MhrMCflhbybizGB15keeeA=="

            porcupine = pvporcupine.create(
                access_key=access_key,
                keyword_paths=['art-o-ditto_en_raspberry-pi_v2_1_0.ppn', 'r-too-d-too_en_raspberry-pi_v2_1_0.ppn'])
            pa = pyaudio.PyAudio()

            audio_stream = pa.open(
                            rate=porcupine.sample_rate,
                            channels=1,
                            format=pyaudio.paInt16,
                            input=True,
                            frames_per_buffer=1024)

            while True:
                pcm = audio_stream.read(porcupine.frame_length)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

                keyword_index = porcupine.process(pcm)

                if keyword_index >= 0:
                    print("keyword detected")
                    # threading.Thread(target=airun).start()


        finally:
            if porcupine is not None:
                porcupine.delete()

            if audio_stream is not None:
                audio_stream.close()

            if pa is not None:
                    pa.terminate()