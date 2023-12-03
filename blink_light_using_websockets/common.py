import os
import sys


def get_raspberry_ip() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    if env_value := os.environ.get("RASPBERRY_IP"):
        return env_value

    return "127.0.0.1"
