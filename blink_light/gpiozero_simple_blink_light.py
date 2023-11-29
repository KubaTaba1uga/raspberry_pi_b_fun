"""
Blinking an LED using GPIOZero.

Dependencies:
  pip3 install gpiozero pigpio

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
from common import get_raspberry_ip
from gpiozero import LED, Device  # (1)
from gpiozero.pins.pigpio import PiGPIOFactory  # (2)


def main():
    Device.pin_factory = PiGPIOFactory(
        host=get_raspberry_ip()
    )  # Set gpiozero to use pigpio by default.      # (3)

    GPIO_PIN = 21
    led = LED(GPIO_PIN)  # (4)
    led.blink(background=False)  # (5)


if __name__ == "__main__":
    main()
