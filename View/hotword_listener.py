import audioop
import math
import threading
import time
import struct
import wave
import pvporcupine
import pyaudio

from DAL.SoundFilePlayer import SoundFilePlayer

class HotwordDetector:
    def __init__(self, access_key: str) -> None:
        self.access_key = access_key

    def wait_for_hotwords(self) -> bool:
        porcupine = None
        python_audio = None
        audio_stream = None

        porcupine = pvporcupine.create(
            access_key=self.access_key,
            keyword_paths=['art-o-ditto_en_raspberry-pi_v2_1_0.ppn', 'r-too-d-too_en_raspberry-pi_v2_1_0.ppn'])
        python_audio = pyaudio.PyAudio()

        audio_stream = python_audio.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=1024
        )

        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                return(True)
