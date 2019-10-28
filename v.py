"""Simple example showing how to get gamepad events."""

from __future__ import print_function


import inputs
import os
from inputs import devices
import glob




def main():
    """Just print out some event infomation when the gamepad is used."""
    key = 'path'
    by_path = glob.glob('/dev/input/by-{key}/*-event-*'.format(key=key))


    for device_path in by_path:
           print(device_path)

#    while 1:
#        events = get_gamepad()
#        for event in events:
#            print(event.ev_type, event.code, event.state)


if __name__ == "__main__":
    main()
