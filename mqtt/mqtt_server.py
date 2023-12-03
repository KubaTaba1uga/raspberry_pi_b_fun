"""
A Python program to .
Server can be combined with websocket_client.py to controll raspberry pi.

Dependencies:
  pip3 install flask flask_socketio

Built and tested with Python 3.7 on Raspberry Pi 3 Model B
"""
import paho.mqtt.client as mqtt
from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)
client = mqtt.Client()


registered_light = "light/0"


@app.route("/led", methods=["GET"])
def get_led_commands():
    return render_template("webpage.html")


@app.route("/led", methods=["POST"])
def post_led_command():
    COMMANDS = ["turn_on", "turn_off", "blink"]

    for command in COMMANDS:
        is_command = request.args.get(command, False)

        if not is_command:
            continue

        client.publish(topic=registered_light, payload=command, qos=0)

        break
    else:
        return "Unrecognized command"

    return "Command executed"


@socketio.event
def led_status(sid, data):
    pass


@socketio.on("connect")
def test_connect():
    print("Client connected", request.sid)


@socketio.on("disconnect")
def test_disconnect():
    print("Client disconnected", request.sid)


def init_mqtt():
    client.on_message = proxy_light_status
    client.on_connect = subscribe_light

    client.connect("localhost", 1883, 60)

    client.loop_start()


def subscribe_light(client, userdata, flags, rc):
    client.subscribe(topic=registered_light + "/status", qos=0)


def proxy_light_status(client, userdata, msg):
    socketio.emit("led status", msg.payload)
    print("Status", msg.payload)


if __name__ == "__main__":
    init_mqtt()
    socketio.run(app, host="0.0.0.0")
