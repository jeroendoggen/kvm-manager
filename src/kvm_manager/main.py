"""
    KVM Manager
    Copyright 2014, Jeroen Doggen, jeroendoggen@gmail.com
"""

import sys

from manager import KVMManager


def run():
    """Run the main program"""
    manager = KVMManager()
    manager.run()
    return(manager.exit_value())


if __name__ == "__main__":
    sys.exit(run())
