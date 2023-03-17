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

    for x in range(100):
        if x % 2 == 0:
            pixels.fill((5, 5, 5))
        else:
            pixels.fill((255, 255, 255))

        time.sleep(0.01)

 

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
                threading.Thread(target=airun).start()


    finally:
        if porcupine is not None:
            porcupine.delete()

        if audio_stream is not None:
            audio_stream.close()

        if pa is not None:
                pa.terminate()


if __name__ == "__main__":
    Speak("R2D2 ONLINE")

    listening_thread = threading.Thread(target=check_internet)
    hello_thread = threading.Thread(target=listening)

    listening_thread.start()
    hello_thread.start()

    listening_thread.join()
    hello_thread.join()
