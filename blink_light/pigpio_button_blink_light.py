"""
Turn on and off an LED with a Button using PiGPIO.

Dependencies:
  pip3 install gpiozero pigpio

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
import signal

import pigpio
from common import get_raspberry_ip

LED_PIN = 21
BUTTON_PIN = 23

pi = pigpio.pi(get_raspberry_ip())


def main():
    pi.set_mode(LED_PIN, pigpio.OUTPUT)
    set_up_button()

    # There are three options available for button:
    #  - FALLING_EDGE callback is called when You pressed the button
    #  - RISING_EDGE callback is called when You released the button
    #  - EITHER_EDGE callback is called when You both press and release the button
    pi.callback(BUTTON_PIN, pigpio.EITHER_EDGE, pressed)


def set_up_button():
    # Configure button pin as an input pin
    pi.set_mode(BUTTON_PIN, pigpio.INPUT)
    # Enable internal pull up resistor
    pi.set_pull_up_down(BUTTON_PIN, pigpio.PUD_UP)
    # Debounce button. When metal meets metal
    #  there is noise produced as byproduct.
    #  Debouncing allow adjusting noise level.
    pi.set_glitch_filter(BUTTON_PIN, 1000)


def pressed(_, __, ___):
    is_light_on = pi.read(LED_PIN)
    state = None

    if is_light_on:
        light_off()
        state = "off"
    else:
        light_on()
        state = "on"

    print(f"Button pressed led is {state}")


def light_off():
    pi.write(LED_PIN, 0)  # 0 = Low = Off


def light_on():
    pi.write(LED_PIN, 1)  # 1 = High = On


if __name__ == "__main__":
    main()

    signal.pause()
