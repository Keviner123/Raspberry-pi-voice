#!/usr/bin/env python3
import pvporcupine
import struct
import pyaudio
import pvporcupine
import pygame
import json
import requests

# AccessKey obtained from Picovoice Console (https://console.picovoice.ai/)
access_key = "KqwUDxJhP+vf3BYnrH3/VXb5Uy2qOr50MhrMCflhbybizGB15keeeA=="

porcupine = None
pa = None
audio_stream = None


handle = pvporcupine.create(
    access_key=access_key,
    keyword_paths=['robot_en_raspberry-pi_v2_1_0.ppn'])



try:
    porcupine = pvporcupine.create(
        access_key=access_key,
        keyword_paths=['robot_en_raspberry-pi_v2_1_0.ppn'])
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

            # Initialize pygame mixer module
            pygame.mixer.init()

            # Load the MP3 file
            pygame.mixer.music.load('ding.mp3')

            # Start playing the MP3 file
            pygame.mixer.music.play()

            # Wait for the MP3 to finish playing
            while pygame.mixer.music.get_busy():
                pass

            # Cleanup the pygame mixer module
            pygame.mixer.quit()
            keyword_index = 0


finally:
    if porcupine is not None:
        porcupine.delete()

    if audio_stream is not None:
        audio_stream.close()

    if pa is not None:
            pa.terminate()
