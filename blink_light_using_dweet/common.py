import hashlib
import os
import sys

DEVICE_ID_SEED = os.environ.get("DWEET_ID_SEED") or "whatever123"


def get_raspberry_ip() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    if env_value := os.environ.get("RASPBERRY_IP"):
        return env_value

    return "127.0.0.1"


def resolve_device_id():
    h = hashlib.new("sha256")  # sha256 can be replaced with diffrent algorithms

    h.update(
        DEVICE_ID_SEED.encode()
    )  # give a encoded string. Makes the String to the Hash

    return h.hexdigest()
