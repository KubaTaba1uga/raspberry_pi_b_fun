"""
A Python program to control an LED using the public dweet.io service.
Led controll is connected to the button. When button is pressed light
is switched on, when button is pressed next time light is switched of.

Dependencies:
  pip3 install gpiozero pigpio requests

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""

import logging
import signal
import sys
from time import sleep

import pigpio
import requests  # (1)
from common import get_raspberry_ip, resolve_device_id

BUTTON_PIN = 23

pi = pigpio.pi(get_raspberry_ip())


logging.basicConfig(level=logging.WARNING)  # Global logging configuration
logger = logging.getLogger("main")  # Logger for this module
logger.setLevel(logging.INFO)


def main():
    print_instructions()

    set_up_button()

    # There are three options available for button:
    #  - FALLING_EDGE callback is called when You pressed the button
    #  - RISING_EDGE callback is called when You released the button
    #  - EITHER_EDGE callback is called when You both press and release the button
    pi.callback(BUTTON_PIN, pigpio.FALLING_EDGE, pressed)


def set_up_button():
    # Configure button pin as an input pin
    pi.set_mode(BUTTON_PIN, pigpio.INPUT)
    # Enable internal pull up resistor
    pi.set_pull_up_down(BUTTON_PIN, pigpio.PUD_UP)
    # Debounce button. When metal meets metal
    #  there is noise produced as byproduct.
    #  Debouncing allow adjusting noise level.
    pi.set_glitch_filter(BUTTON_PIN, 1000)


def persist_led(func):
    led = {"state": None}

    def wrapped(*args, **kwargs):
        kwargs["last_led_state"] = led["state"]

        led["state"] = func(*args, **kwargs)

    return wrapped


@persist_led
def pressed(*args, **kwargs):
    is_light_on = kwargs.get("last_led_state")

    if not is_light_on:
        light_on()
        is_light_on = 1
    else:
        light_off()
        is_light_on = 0

    logger.info(f"Button pressed led is {is_light_on}")

    return is_light_on


def light_off():
    url = "https://dweet.io/dweet/for/{}?state=off".format(resolve_device_id())

    result = requests.get(url)

    logger.debug("Response for button press was %s", result.status_code)


def light_on():
    url = "https://dweet.io/dweet/for/{}?state=on".format(resolve_device_id())

    result = requests.get(url)

    logger.debug("Response for button press was %s", result.status_code)


def print_instructions():
    """Print instructions to terminal."""
    print("LED Control via Button - Try pressing the button.")


if __name__ == "__main__":

    def signal_handler(sig, frame):
        light_off()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)  # Capture CTRL + C

    main()

    signal.pause()
