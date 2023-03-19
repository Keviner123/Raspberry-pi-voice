import subprocess

class Accesspoint:
    def __init__(self, ssid: str, password: str) -> None:
        self.ssid = ssid
        self.password = password
    def start(self):
        subprocess.Popen(["create_ap", "wlan0", "eth0", self.ssid, self.password, "--dhcp-dns", "192.168.4.1"])
