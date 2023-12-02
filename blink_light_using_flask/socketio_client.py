import socketio

SECRET = "abcvbcbcbcbcbc"

# standard Python
with socketio.SimpleClient() as sio:
    sio.connect("http://localhost:5000", auth={"secret": SECRET})

    while True:
        event = sio.receive()
        print(f'received event: "{event[0]}" with arguments {event[1:]}')
