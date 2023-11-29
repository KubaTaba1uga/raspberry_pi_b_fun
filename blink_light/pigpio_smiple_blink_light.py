"""
Blinking an LED using PiGPIO.

Dependencies:
  pip3 install pigpio

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
from time import sleep

import pigpio
from common import get_raspberry_ip

GPIO_PIN = 21


def main():
    pi = pigpio.pi(get_raspberry_ip())  # (2)
    pi.set_mode(GPIO_PIN, pigpio.OUTPUT)  # (3)

    while True:
        try:
            blink(pi)
        except KeyboardInterrupt:
            light_off(pi)
            break


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
