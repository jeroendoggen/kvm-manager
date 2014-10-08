"""
    KVM Manager
    Copyright 2014, Jeroen Doggen, jeroendoggen@gmail.com
"""


from __future__ import print_function, division  # We require Python 2.6+

import os

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

    def run(self):
        #""" Run the program (call this from main) """
        for x in range(0, self.settings.number_of_servers):
            self.setup_server(x)

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
        print("Starting server: " + str(servername))

    def stop_server(self, servername):
        print("Stopping server: " + str(servername))

    def clone_server(self, servername):
        print("Cloning server: " + str(servername))
