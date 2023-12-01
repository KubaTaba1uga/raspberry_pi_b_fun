from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)


@app.route("/led", methods=["GET"])
def get_led_commands():
    return render_template("webpage.html")


@app.route("/led", methods=["POST"])
def post_led_command():
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0")
