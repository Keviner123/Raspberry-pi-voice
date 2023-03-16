import threading
import time
import urllib.request
import neopixel
import board
from flask import Flask, render_template, request
import subprocess
import subprocess
import time


pixels = neopixel.NeoPixel(board.D18, 60)


create_ap_process = None


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


    return("Rebooting...")
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

            set_wifi_connection(ssid, password)

            create_ap_process.terminate()
            pixels.fill((0, 0, 0))



        return render_template('index.html')



    app.run(host="0.0.0.0", port="8000")

def check_internet():
    global create_ap_process

    ap_is_up = False

    while True:
        try:
            urllib.request.urlopen("http://www.google.com")

            pixels.fill((0, 0, 10))
            try:
                ap_is_up = False
                create_ap_process.terminate()
            except:
                pass


        except urllib.error.URLError:
            print("No internet connection.")
            pixels.fill((10, 0, 0))

            if(ap_is_up == False):
                print("Creating AP")
                args = ["create_ap", "wlan0", "eth0", "R2D2-Config", "12345678", "--dhcp-dns", "192.168.4.1"]
                create_ap_process = subprocess.Popen(args)
                ap_is_up = True
                time.sleep(3)
                start_webserver()

        print("Checking connection")
        time.sleep(1)

def print_hello_world():
    while True:
        time.sleep(1)

if __name__ == "__main__":
    internet_thread = threading.Thread(target=check_internet)
    hello_thread = threading.Thread(target=print_hello_world)

    internet_thread.start()
    hello_thread.start()

    internet_thread.join()
    hello_thread.join()