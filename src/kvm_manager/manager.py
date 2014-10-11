"""
    KVM Manager
    Copyright 2014, Jeroen Doggen, jeroendoggen@gmail.com
"""


from __future__ import print_function, division  # We require Python 2.6+

import os
import SocketServer
import multiprocessing
import time

from settings import Settings
from logger import Logger
from reporter import Reporter
from server import UDPHandler


class KVMManager:
    """ Contains all the tools to manage KVM servers"""

    def __init__(self):
        self.settings = Settings()
        self.logger = Logger(self.settings.logfile)
        self.reporter = Reporter(self.settings)
        #self.setup = Setup(self.settings, self.logger)
        self.errors = 0
        servernumber = 0
        #TODO define in config file
        self.host = "localhost"
        self.port = 9999
        self.server = 0

    def run(self):
        """ Run the program (call this from main) """
        #
        if self.settings.actions.create:
            print("create")
            self.create_servers()
        if self.settings.actions.start:
            print("start")
            self.start_servers()
            self.start_listener()
        if self.settings.actions.stop:
            print("stop")
            self.stop_servers()
        if self.settings.actions.destroy:
            print("destroy")
            self.destroy_servers()
        if self.settings.actions.delete:
            print("delete")
            self.delete_servers()

    def start_listener(self):
        file = open("../../virtual-servers.html", "w")
        #file.write("")
        file.close()
        self.server = SocketServer.UDPServer((self.host, self.port), UDPHandler)
        process = multiprocessing.Process(target=self.server.serve_forever)
        process.daemon = True
        process.start()
        # Wait for servers to boot -> to write the list with IP addresses.
        # TODO implement this nicer
        time.sleep(60)

    def handle_reqs(self):
        self.server.handle_request

    def create_servers(self):
        for servernumber in range(0, self.settings.number_of_servers):
            self.create_server(self.settings.source_image, servernumber)

    def create_server(self, servername, servernumber):
        print("Cloning server: " + str(servername + str(servernumber)))
        os.system("virt-clone --connect qemu:///system  --original " + servername + " --name clone" + str(servernumber) + " --auto-clone")

    def start_servers(self):
        for servernumber in range(0, self.settings.number_of_servers):
            self.start_server(self.settings.source_image, servernumber)

    def start_server(self, servername, servernumber):
        print("Starting server: " + str(servername + str(servernumber)))
        os.system("virsh --connect qemu:///system start clone" + str(servernumber))

    def stop_servers(self):
        for servernumber in range(0, self.settings.number_of_servers):
            self.stop_server(self.settings.source_image, servernumber)

    def stop_server(self, servername, servernumber):
        print("Stopping server: " + str(servername + str(servernumber)))
        os.system("virsh --connect qemu:///system shutdown clone" + str(servernumber))
        #os.system("virsh --connect qemu:///system destroy clone" + str(servernumber))

    def delete_servers(self):
        for servernumber in range(0, self.settings.number_of_servers):
            self.delete_server(self.settings.source_image, servernumber)

    def delete_server(self, servername, servernumber):
        print("Stopping server: " + str(servername + str(servernumber)))
        os.system("virsh --connect qemu:///system undefine clone" + str(servernumber))
        # TODO delete image files (owned by root on Debian!?)

    def destroy_servers(self):
        """ The equivalent of ripping the power cord out of the physical machines."""
        for servernumber in range(0, self.settings.number_of_servers):
            self.destroy_server(self.settings.source_image, servernumber)

    def destroy_server(self, servername, servernumber):
        print("Stopping server: " + str(servername + str(servernumber)))
        os.system("virsh --connect qemu:///system destroy clone" + str(servernumber))

    def exit_value(self):
        #"""TODO: Generate the exit value for the application."""
        if (self.errors == 0):
            return 0
        else:
            return 42

    def create_ip_list(self):
        pass
