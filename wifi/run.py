from flask import Flask, render_template, request
import subprocess
import time

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

    time.sleep(5)

    subprocess.run(['sudo reboot'])

    time.sleep(5)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f'Username: {username}, Password: {password}')
        set_wifi_connection()
    return render_template('index.html')



if __name__ == '__main__':
    args = ["create_ap", "wlan0", "eth0", "YourSSID", "12345678", "--dhcp-dns", "192.168.4.1"]
    create_ap_process = subprocess.Popen(args)

    time.sleep(5)

    app.run(host="0.0.0.0", port="80")
    create_ap_process.terminate()
