#!/usr/bin/env python3

from functools import partial
import sys
import subprocess
import pyudev   # give me udev wrapper
                # requires installing pyudev through pip

def main():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='usb')
    monitor.start()

    # for device in iter( monitor.poll, None ):
    #     # get sequence of relevant USB storage devices
    #     print(device.sys_path)

    # This new version avoids invocating the `external` system call by waiting until no other events occur.
    # https://unix.stackexchange.com/questions/65891/how-to-execute-a-shellscript-when-i-plug-in-a-usb-device
    device = monitor.poll( timeout=None )
    for device in iter( partial( monitor.poll, 1 ), None ):
        # device specific calls happen here
        pass
    # generic calls happen here

if __name__ == '__main__':
    try:
        main()
    except (BrokenPipeError, KeyboardInterrupt) as e:
        # avoid additional broken pipe errors. https://stackoverflow.com/a/26738736
        sys.stderr.close()
        exit(e.errno)