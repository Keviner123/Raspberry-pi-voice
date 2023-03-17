import flask
import subprocess
from flask import render_template, request
from DAL.WifiConfigFile import WifiConfigFile

class Webserver:
    def __init__(self, port:int):
        self.port = port
        pass

    def start_webserver(self):
        app = flask.Flask(__name__, template_folder='../templates/')

        @app.route('/', methods=['GET', 'POST'])
        def index():
            if request.method == 'POST':
                ssid = request.form['ssid']
                password = request.form['password']

                wcf = WifiConfigFile("/etc/wpa_supplicant/wpa_supplicant.conf")
                wcf.update_config_file(ssid, password)
                subprocess.call(['sudo', 'reboot'])



                return(":)")
            return render_template('index.html')

        app.run(host="0.0.0.0", port=self.port)
