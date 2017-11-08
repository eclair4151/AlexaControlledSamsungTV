from flask import Flask
from pywakeonlan import send_magic_packet
import samsungctl
import config
from flask import jsonify
import time


app = Flask(__name__)

remote_config = {
    "name": "samsungctl",
    "description": "PC",
    "id": "",
    "host": config.host,
    "port": config.port,
    "method": config.method,
    "timeout": 0,
}

@app.route('/turn_on')
def turn_on():
    send_magic_packet(config.tv_mac_address)
    time.sleep(3)
    with samsungctl.Remote(remote_config) as remote:
        remote.control("KEY_RETURN")  #get rid of the on menu when you turn the tv on

    return jsonify({"status": 200})


@app.route('/mute')
def mute():
    with samsungctl.Remote(remote_config) as remote:
        remote.control("KEY_MUTE")
    return jsonify({"status": 200})


@app.route('/turn_off')
def turn_off():
    with samsungctl.Remote(remote_config) as remote:
        remote.control("KEY_POWER")
    return jsonify({"status": 200})


if __name__ == '__main__':
    app.run()