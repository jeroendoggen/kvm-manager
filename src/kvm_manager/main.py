"""
    KVM Manager
    Copyright 2014, Jeroen Doggen, jeroendoggen@gmail.com
"""

import sys
import signal

from manager import KVMManager


def run():
    """Run the main program"""
    signal.signal(signal.SIGINT, signal_handler)
    manager = KVMManager()
    manager.run()
    return(manager.exit_value())

def signal_handler(signal, frame):
        sys.exit(0)

if __name__ == "__main__":
    sys.exit(run())
