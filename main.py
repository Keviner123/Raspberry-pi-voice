#!/usr/bin/env python3
import struct
import pyaudio
import pvporcupine
import pygame
import json
import requests
import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 60)
pixels.fill((0, 0, 0))



def stupidrun():
    import pyaudio
    import wave
    import audioop
    import math

    # Set the silence threshold value (in dB)
    THRESHOLD = 50

    # Set the chunk size and recording duration
    CHUNK_SIZE = 1024
    RECORD_DURATION = 10  # in seconds

    # Set the PyAudio parameters
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    # Create the PyAudio object
    audio = pyaudio.PyAudio()

    # Open the default input device for recording
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK_SIZE)

    # Initialize variables for the output file and the silence counter
    output_file = wave.open('output.wav', 'wb')
    output_file.setnchannels(1)
    output_file.setsampwidth(audio.get_sample_size(FORMAT))
    output_file.setframerate(RATE)

    silence_counter = 0

    # Record audio until there is silence
    while silence_counter < 50:  # adjust this value to set the minimum silence duration in frames
        # Read a chunk of audio data from the input stream
        data = stream.read(CHUNK_SIZE)

        # Compute the RMS amplitude of the audio data (in dB)
        rms = audioop.rms(data, 2)
        db = 20 * math.log10(rms) if rms > 0 else 0

        # Write the audio data to the output file
        output_file.writeframes(data)

        # Check if the audio is silent
        if db < THRESHOLD:
            silence_counter += 1
        else:
            silence_counter = 0

        # Log the dB value
        print(f"dB: {db:.2f}")





    # Close the output file and the input stream
    output_file.close()
    stream.stop_stream()
    stream.close()
    audio.terminate()




    from google.cloud import speech
    import os
    import io


    #setting Google credential
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']= 'login.json'
    # create client instance
    client = speech.SpeechClient()

    #the path of your audio file
    file_name = "output.wav"
    with io.open(file_name, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)


    config = speech.RecognitionConfig(
        encoding = 'LINEAR16',
        language_code = 'da-DK',
        sample_rate_hertz = 44100,
        audio_channel_count = 1,
    )

    # Sends the request to google to transcribe the audio
    response = client.recognize(request={"config": config, "audio": audio})




    # Import the required module for text
    # to speech conversion
    from gtts import gTTS
    import pygame

    # This module is imported so that we can
    # play the converted audio
    import os



    mytext = response.results[0].alternatives[0].transcript
    print(mytext)



    url = "http://192.168.1.128:8000/AskQuestion"

    payload = json.dumps({
    "Question": mytext
    })
    headers = {
    'Content-Type': 'application/json'
    }

    print(str(payload))

    response = requests.request("GET", url, headers=headers, data=payload, timeout=60)

    # The text that you want to convert to audio


    # Language in which you want to convert
    # Passing the text and language to the engine,
    # here we have marked slow=False. Which tells
    # the module that the converted audio should
    # have a high speed
    myobj = gTTS(text=response.text, lang='da', slow=False)

    # Saving the converted audio in a mp3 file named
    # welcome
    myobj.save("output.mp3")


    # Initialize pygame mixer module
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('output.mp3')

    # Start playing the MP3 file
    pygame.mixer.music.play()

    # Wait for the MP3 to finish playing
    while pygame.mixer.music.get_busy():
        pass

    # Cleanup the pygame mixer module
    pygame.mixer.quit()


porcupine = None
pa = None
audio_stream = None

try:
    access_key = "KqwUDxJhP+vf3BYnrH3/VXb5Uy2qOr50MhrMCflhbybizGB15keeeA=="


    porcupine = pvporcupine.create(
        access_key=access_key,
        keyword_paths=['art-o-ditto_en_raspberry-pi_v2_1_0'])
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

            stupidrun()

finally:
    if porcupine is not None:
        porcupine.delete()

    if audio_stream is not None:
        audio_stream.close()

    if pa is not None:
            pa.terminate()
