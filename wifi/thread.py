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


def set_wifi_connection():

    # Generate the wpa_supplicant.conf file content
    wpa_supplicant_conf = '''
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1

    network={
            ssid="internet"
            psk="Kode123!"
    }
    '''

    # Write the wpa_supplicant.conf file to disk
    with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'w') as f:
        f.write(wpa_supplicant_conf)

    pixels.fill((0, 0, 0))

    subprocess.call(['sudo', 'reboot'])

def start_webserver():

    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            ssid = request.form['ssid']
            password = request.form['password']
            print(f'ssid: {ssid}, Password: {password}')
            set_wifi_connection()
        return render_template('index.html')


    if __name__ == '__main__':
        # args = ["create_ap", "wlan0", "eth0", "YourSSID", "12345678", "--dhcp-dns", "192.168.4.1"]
        # create_ap_process = subprocess.Popen(args)

        time.sleep(5)

        app.run(host="0.0.0.0", port="80")
        create_ap_process.terminate()



def check_internet():
    create_ap_process = None

    ap_is_up = False

    while True:
        try:
            urllib.request.urlopen("http://www.google.com")
            print("Internet is available.")
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
                args = ["create_ap", "wlan0", "eth0", "R2D2-Config", "12345678", "--dhcp-dns", "192.168.4.1"]
                create_ap_process = subprocess.Popen(args)
                ap_is_up = True
                start_webserver()


        time.sleep(1)

def print_hello_world():
    while True:
        print("Hello, world!")
        time.sleep(1)

if __name__ == "__main__":
    internet_thread = threading.Thread(target=check_internet)
    hello_thread = threading.Thread(target=print_hello_world)

    internet_thread.start()
    hello_thread.start()

    internet_thread.join()
    hello_thread.join()