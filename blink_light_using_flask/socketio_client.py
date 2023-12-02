from time import sleep

import socketio
from common import get_raspberry_ip
from gpiozero import LED, Device  # (1)
from gpiozero.pins.pigpio import PiGPIOFactory  # (2)

SECRET = "abcvbcbcbcbcbc"

Device.pin_factory = PiGPIOFactory(host=get_raspberry_ip())

GPIO_PIN = 21
led = LED(GPIO_PIN)


def main():
    with socketio.SimpleClient() as sio:
        sio.connect(
            "http://localhost:5000", auth={"secret": SECRET}, transports=["websocket"]
        )

        while True:
            event = sio.receive()

            event_name = event[0]

            if event_name == "led command":
                handle_light_command(event[1])


def handle_light_command(command):
    COMMANDS_FUNCS_MAP = {
        "turn_on": lambda: led.on(),
        "turn_off": lambda: led.off(),
        "blink": blink_light,
    }

    func = COMMANDS_FUNCS_MAP.get(command)

    if not func:
        return

    func()


def blink_light():
    led.on()
    sleep(1)
    led.off()


if __name__ == "__main__":
    main()
