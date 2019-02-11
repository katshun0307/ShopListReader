# -*- coding: utf-8 -*- #

""" read barcode reader input
"""

import struct
from concurrent.futures import ThreadPoolExecutor
import control
import config

code_to_num = {
    "458782": "1",
    "458783": "2",
    "458784": "3",
    "458785": "4",
    "458786": "5",
    "458787": "6",
    "458788": "7",
    "458789": "8",
    "458790": "9",
    "458791": "0",
}

executor = ThreadPoolExecutor(max_workers=2)


def decode_jan(key_code_list):
    jan_code = int("".join([code_to_num[code] for code in key_code_list]))
    return jan_code


def wait():
    # modulo 4 counter
    counter = 0
    # list of key codes
    current_keycode_list = []

    while True:
        try:
            with open('/dev/input/event0', 'rb') as fp:
                while True:
                    # while event0 is open
                    buffer = fp.read(24)
                    key = struct.unpack('4IHHI', buffer)[3]
                    if counter is 0 and int(key) == 458792:
                        # finish current input
                        jan = decode_jan(current_keycode_list)
                        if jan == config.TRASH_CODE:
                            config.mode = "trash"
                            print("current mode is trash")
                        elif jan == config.SHOP_CODE:
                            config.mode = "shop"
                            print("current mode is shop")
                        else:
                            executor.submit(control.process, jan)
                        current_keycode_list = []  # refresh current jan
                    elif counter is 0:
                        current_keycode_list.append(str(key))
                    else:
                        pass
                    counter = (counter + 1) % 4
        except (OSError, FileNotFoundError):
            pass  # device disconnected


if __name__ == '__main__':
    wait()
