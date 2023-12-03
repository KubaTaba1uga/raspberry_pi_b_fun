"""
A Python program to controll a led via MQTT messages.
Client creates subscription on `light/0` topic.
There are three commands that cen be sent to the client:
 - turn_on
 - turn_off
 - blink

Dependencies:
  pip3 install paho-mqtt gpiozero

Built and tested with Python 3.7 on Raspberry Pi 3 Model B
"""
import logging
from collections import deque
from time import sleep

import paho.mqtt.client as mqtt
from common import get_raspberry_ip
from gpiozero import LED, Device
from gpiozero.pins.pigpio import PiGPIOFactory

DEVICE_ID = "light/0"
GPIO_PIN = 21
SLEEP_TIME = 0.01

# Initialize Logging
logging.basicConfig(level=logging.WARNING)  # Global logging configuration
logger = logging.getLogger("main")  # Logger for this module
logger.setLevel(logging.INFO)

# Configure GPIO
Device.pin_factory = PiGPIOFactory(host=get_raspberry_ip())
led = LED(GPIO_PIN)

# Create tasks queue
command_tasks = deque()


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost", 1883, 60)

    while True:
        client.loop(timeout=0.5)

        publish_status(client)

        process_tasks(client)

        sleep(SLEEP_TIME)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic=DEVICE_ID, qos=0)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    logger.info("Received message: " + msg.topic + " " + str(msg.payload))

    command_tasks.append(
        (
            handle_light_command,
            [msg.payload.decode("utf-8")],
        )
    )


def publish_status(client):
    status = "on" if led.value else "off"

    logger.debug("Sending status: " + status)

    client.publish(topic=DEVICE_ID + "/status", payload=status, qos=0)


def process_tasks(client):
    try:
        command_task = command_tasks.popleft()
    except IndexError:
        return

    task, args = command_task

    logger.debug("Processing: %s(%s)", task, args)

    task(*args)


def handle_light_command(command):
    COMMANDS_FUNCS_MAP = {
        "turn_on": led.on,
        "turn_off": led.off,
        "blink": blink_light,
    }

    func = COMMANDS_FUNCS_MAP.get(command)

    if not func:
        return

    command_tasks.append(
        (
            func,
            [],
        )
    )


def blink_light():
    BLINKING_TIME_IN_SECONDS = 2

    for i in range(int(BLINKING_TIME_IN_SECONDS / SLEEP_TIME)):
        command_tasks.appendleft(
            (
                wait,
                [],
            )
        )

    command_tasks.appendleft(
        (
            led.on,
            [],
        )
    )

    command_tasks.insert(
        i + 2,
        (
            led.off,
            [],
        ),
    )


def wait():
    pass


if __name__ == "__main__":
    main()
