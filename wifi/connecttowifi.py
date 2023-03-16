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
