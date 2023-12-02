from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)

registered_lights = {}


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

        for light_id in registered_lights:
            socketio.emit("led command", command, room=light_id)

        break
    else:
        return "Unrecognized command"

    return "Command executed"


@socketio.event
def led_command(sid, data):
    pass


@socketio.on("connect")
def test_connect(auth):
    SECRET = "abcvbcbcbcbcbc"

    if len(registered_lights) > 0:
        return

    if auth.get("secret") != SECRET:
        return

    registered_lights[request.sid] = True

    print("Client connected", request.sid)


@socketio.on("disconnect")
def test_disconnect():
    registered_lights.pop(request.sid, None)

    print("Client disconnected", request.sid)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0")
