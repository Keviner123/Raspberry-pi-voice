class WifiConfigFile:
    def __init__(self, file_path: str):
        self.file_path = file_path
        
    def update_config_file(self, ssid: str, psk: str):
        wpa_supplicant_conf = f'''
        ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
        update_config=1

        network={{
                ssid="{ssid}"
                psk="{psk}"
        }}
        '''

        with open(self.file_path, 'w') as f:
            f.write(wpa_supplicant_conf)
