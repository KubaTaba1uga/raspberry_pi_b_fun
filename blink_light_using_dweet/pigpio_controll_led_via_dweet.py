"""
A Python program to control an LED using the public dweet.io service.

Dependencies:
  pip3 install gpiozero pigpio requests

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
import hashlib
import logging
import signal
import sys
from time import sleep

import pigpio
import requests  # (1)
from common import get_raspberry_ip

GPIO_PIN = 21
URL = "https://dweet.io"  # Dweet.io service API
DEVICE_ID_SEED = "whatever123"

dweets_cache = {}

logging.basicConfig(level=logging.WARNING)  # Global logging configuration
logger = logging.getLogger("main")  # Logger for this module
logger.setLevel(logging.INFO)


def main():
    pi = create_gpio_controller()

    def signal_handler(sig, frame):
        light_off(pi)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)  # Capture CTRL + C

    device_id = resolve_device_id()

    print_instructions(device_id)

    # Initialise LED from last dweet.
    last_dweet = get_latest_dweet(device_id)
    if last_dweet:
        process_dweet(pi, last_dweet)

    print("Waiting for dweets. Press Control+C to exit.")

    poll_dweets_forever(
        pi, device_id, delay_secs=2
    )  # Get dweets by polling a URL on a schedule.            # (19)


def create_gpio_controller():
    pi = pigpio.pi(get_raspberry_ip())  # (2)
    pi.set_mode(GPIO_PIN, pigpio.OUTPUT)  # (3)

    return pi


def print_instructions(device_id):
    """Print instructions to terminal."""
    print("LED Control URLs - Try them in your web browser:")
    print("  On    : " + URL + "/dweet/for/" + device_id + "?state=on")
    print("  Off   : " + URL + "/dweet/for/" + device_id + "?state=off")
    print("  Blink : " + URL + "/dweet/for/" + device_id + "?state=blink\n")


def get_latest_dweet(device_id):
    """Get the last dweet made by our thing."""
    resource = URL + "/get/latest/dweet/for/" + device_id
    logger.debug("Getting last dweet from url %s", resource)

    r = requests.get(resource)  # (7)

    if r.status_code == 200:  # (8)
        dweet = r.json()  # return a Python dict.
        logger.debug("Last dweet for thing was %s", dweet)

        dweet_content = None

        if dweet["this"] == "succeeded":  # (9)
            creation_time = dweet["with"][0]["created"]

            if dweets_cache.get(creation_time):
                return dweet_content

            dweets_cache[creation_time] = True

            # We're just interested in the dweet content property.
            dweet_content = dweet["with"][0]["content"]  # (10)

        return dweet_content

    else:
        logger.error("Getting last dweet failed with http status %s", r.status_code)
        return {}


def persist_led(func):
    led = {"state": None}

    def wrapped(*args, **kwargs):
        kwargs["last_led_state"] = led["state"]

        led["state"] = func(*args, **kwargs)

    return wrapped


@persist_led
def process_dweet(pi, dweet, last_led_state=None):
    """Inspect the dweet and set LED state accordingly"""

    if not (led_state := dweet.get("state")):
        return

    if (
        last_led_state == led_state and led_state != "blink"
    ):  # Blink should be repetable
        return

    if led_state == "blink":
        blink(pi)
    elif led_state == "on":  # (15)
        light_on(pi)
    elif led_state == "off":
        light_off(pi)
    else:
        led_state = "unrecognized"

    logger.info("LED " + led_state)

    return led_state


def poll_dweets_forever(pi, device_id, delay_secs=2):
    """Poll dweet.io for dweets about our thing."""
    while True:
        dweet = get_latest_dweet(device_id)  # (11)

        if dweet is None:
            continue

        process_dweet(pi, dweet)  # (12)

        sleep(delay_secs)  # (13)


def resolve_device_id():
    h = hashlib.new("sha256")  # sha256 can be replaced with diffrent algorithms

    h.update(
        DEVICE_ID_SEED.encode()
    )  # give a encoded string. Makes the String to the Hash

    return h.hexdigest()


def blink(pi):
    light_on(pi)
    sleep(1.8)
    light_off(pi)
    sleep(1)


def light_on(pi):
    pi.write(GPIO_PIN, 1)  # 1 = High = On      # (4)


def light_off(pi):
    pi.write(GPIO_PIN, 0)  # 0 = Low = Off      # (5)


if __name__ == "__main__":
    main()
