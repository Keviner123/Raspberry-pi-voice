#!/usr/bin/env python3
import struct
import pyaudio
import pvporcupine

porcupine = None
pa = None
audio_stream = None

try:
    porcupine = pvporcupine.create(access_key="KqwUDxJhP+vf3BYnrH3/VXb5Uy2qOr50MhrMCflhbybizGB15keeeA==",keywords=["blueberry","hey google", "jarvis"])

    pa = pyaudio.PyAudio()

    audio_stream = pa.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length)

    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:
            print("Hotword Detected")

            pygame.mixer.init()
            sound = pygame.mixer.Sound('ding.wav')
            playing = sound.play()


finally:
    if porcupine is not None:
        porcupine.delete()

    if audio_stream is not None:
        audio_stream.close()

    if pa is not None:
            pa.terminate()
