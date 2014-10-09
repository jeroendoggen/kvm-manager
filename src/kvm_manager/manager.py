"""
    KVM Manager
    Copyright 2014, Jeroen Doggen, jeroendoggen@gmail.com
"""


from __future__ import print_function, division  # We require Python 2.6+

import os
import sys

from settings import Settings
from logger import Logger
from reporter import Reporter
from setup import Setup


class KVMManager:
    """ Contains all the tools to manage KVM servers"""

    def __init__(self):
        self.settings = Settings()
        self.logger = Logger(self.settings.logfile)
        self.reporter = Reporter(self.settings)
        self.setup = Setup(self.settings, self.logger)
        self.errors = 0
        self.counter = 0

    def run(self):
        """ Run the program (call this from main) """
        #self.start_servers()
        self.stop_servers()

    def start_servers(self):
        for x in range(0, self.settings.number_of_servers):
            self.setup_server(self.settings.source_image)
            self.counter = self.counter + 1

    def stop_servers(self):
        for x in range(0, self.settings.number_of_servers):
            self.stop_server(self.settings.source_image)
            self.counter = self.counter + 1


    def exit_value(self):
        #"""TODO: Generate the exit value for the application."""
        if (self.errors == 0):
            return 0
        else:
            return 42

    def setup_server(self, servername):
        self.clone_server(servername)
        self.start_server(servername)

    def start_server(self, servername):
        print("Starting server: " + str(servername + str(self.counter)))
        os.system("virsh --connect qemu:///system start clone" + str(self.counter))

    def stop_server(self, servername):
        print("Stopping server: " + str(servername + str(self.counter)))
        os.system("virsh --connect qemu:///system shutdown clone" + str(self.counter))

    def clone_server(self, servername):
        print("Cloning server: " + str(servername + str(self.counter)))
        os.system("virt-clone --connect qemu:///system  --original " + servername + " --name clone" + str(self.counter) + " --auto-clone")
