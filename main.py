#!/usr/bin/env python3

import threading
import urllib.request
from flask import Flask, render_template, request
import subprocess
import time
import struct
import pyaudio
import pvporcupine
import pygame
import json
import requests
import board
import neopixel
import wave
import audioop
import math
from google.cloud import speech
import os
import io
from gtts import gTTS

pixels = neopixel.NeoPixel(board.D18, 60)

create_ap_process = None

def Speak(text: str):
    os.system('espeak -vda "'+text+'"')


def airun():
    print("Hotword Detected")

    pixels.fill((100, 100, 100))


    pygame.mixer.init()
    sound = pygame.mixer.Sound('assets\ding.wav')
    playing = sound.play()


    # Set the silence threshold value (in dB)
    THRESHOLD = 60

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

    mytext = response.results[0].alternatives[0].transcript
    print(mytext)

    url = "https://api.xn--prve-hra.xn--svendeprven-ngb.dk/api/question/device?question="+mytext

    payload={}
    headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6IjMiLCJleHAiOjE3MTA1MDE4MDMsImlzcyI6InRlc3QtZXhhbS1hcGkifQ.9boMBfPswAjOZUo5ZcCLmSnNgk4elePBhGPZPVnOFrk'
    }


    print(str(payload))

    response = requests.request("GET", url, headers=headers, data=payload, timeout=60)
    response = json.loads(response.text)


    # myobj = gTTS(text=response["answer"], lang='da', slow=False)
    # os.system('espeak -vda "'+response["answer"]+'"')
    Speak(response["answer"])


    myobj.save("output.mp3")

    # pixels.fill((0, 0, 255))


    pygame.mixer.init()

    pygame.mixer.music.load('output.mp3')

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pass

    pygame.mixer.quit()
    pixels.fill((0, 0, 0))

def set_wifi_connection(ssid: str, psk: str):

    wpa_supplicant_conf = '''
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1

    network={
            ssid="'''+ssid+'''"
            psk=="'''+psk+'''"
    }
    '''

    with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as f:
        f.write(wpa_supplicant_conf)

    subprocess.call(['sudo', 'reboot'])

def start_webserver():
    print("STARTING WEBSERVER")

    global pixels
    global create_ap_process

    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            ssid = request.form['ssid']
            password = request.form['password']


            create_ap_process.terminate()
            pixels.fill((0, 0, 0))
            Speak("R2D2 genstarter")

            set_wifi_connection(ssid, password)



        return render_template('index.html')



    app.run(host="0.0.0.0", port="8000")

def check_internet():
    global create_ap_process

    ap_is_up = False

    while True:
        try:
            urllib.request.urlopen("http://www.google.com")

            try:
                ap_is_up = False
                create_ap_process.terminate()
            except:
                pass


        except urllib.error.URLError:
            print("No internet connection.")
            pixels.fill((10, 0, 0))
            Speak("Adgang til internet fraforbundet")


            if(ap_is_up == False):
                print("Creating AP")
                args = ["create_ap", "wlan0", "eth0", "R2D2-Config", "12345678", "--dhcp-dns", "192.168.4.1"]
                create_ap_process = subprocess.Popen(args)
                ap_is_up = True
                time.sleep(3)
                start_webserver()

        time.sleep(1)

def listening():

    porcupine = None
    pa = None
    audio_stream = None

    try:
        access_key = "KqwUDxJhP+vf3BYnrH3/VXb5Uy2qOr50MhrMCflhbybizGB15keeeA=="


        porcupine = pvporcupine.create(
            access_key=access_key,
            keyword_paths=['art-o-ditto_en_raspberry-pi_v2_1_0.ppn'])
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
                threading.Thread(target=airun).start()


    finally:
        if porcupine is not None:
            porcupine.delete()

        if audio_stream is not None:
            audio_stream.close()

        if pa is not None:
                pa.terminate()


if __name__ == "__main__":
    listening_thread = threading.Thread(target=check_internet)
    hello_thread = threading.Thread(target=listening)

    listening_thread.start()
    hello_thread.start()

    listening_thread.join()
    hello_thread.join()
