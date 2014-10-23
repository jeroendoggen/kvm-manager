"""
    KVM Manager
    Copyright 2014, Jeroen Doggen, jeroendoggen@gmail.com
"""


from __future__ import print_function, division  # We require Python 2.6+

import os
import SocketServer
import multiprocessing
import time
import math
import socket

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
        #self.host = socket.gethostbyname(socket.gethostname())
        self.host = "localhost"
        self.port = 9999
        self.server = 0
        self.server_state = 256
        self.running_servers = 0

    def run(self):
        """ Run the program (call this from main) """
        #
        self.settings.last_server = self.settings.first_server + self.settings.number_of_servers
        self.print_info()
        if self.settings.actions.create:
            print("create")
            self.create_servers()
        if self.settings.actions.start:
            print("start")
            self.start_servers()
        if self.settings.actions.stop:
            print("stop")
            self.stop_servers()
        if self.settings.actions.destroy:
            print("destroy")
            self.destroy_servers()
        if self.settings.actions.delete:
            print("delete")
            self.delete_servers()
        if self.settings.actions.listen:
            print("Start listening for servers:")
            self.start_listener()

    def start_listener(self):
        # TODO move to config file
        file = open("../../virtual-servers.html", "w")
        #file.write("")
        file.close()
        self.server = SocketServer.UDPServer((self.host, self.port), UDPHandler)
        process = multiprocessing.Process(target=self.server.serve_forever)
        process.daemon = True
        process.start()
        # Wait for servers to boot -> to write the list with IP addresses.
        # TODO implement this nicer
        print("Press ctrl-c to stop")
        # Keep listening forever
        while True:
            time.sleep(1)
            #self.reporter.run()

    def handle_reqs(self):
        self.server.handle_request

    def create_servers(self):
        for servernumber in range(self.settings.first_server, self.settings.last_server):
            self.create_server(self.settings.source_image, servernumber)

    def create_server(self, servername, servernumber):
        print("Cloning server: " + str(servername + str(servernumber)))
        os.system("virt-clone --connect qemu:///system  --original " + servername + " --name clone" + str(servernumber) + " --auto-clone")

    def start_servers(self):
        for servernumber in range(self.settings.first_server, self.settings.last_server):
            self.start_server(self.settings.source_image, servernumber)

    def start_server(self, servername, servernumber):
	print("Starting server: " + str(servername + str(servernumber)))
	self.server_state = os.system("virsh --connect qemu:///system start clone" + str(servernumber))
        if self.server_state is 256:
            self.running_servers = self.running_servers + 1
        servercount = - (self.settings.first_server - servernumber) - self.running_servers + 1
        # To avoid starving CPU & IO resources (boot time scale approx. like that)(empirical!)
        if self.server_state is not 256:
            sleeptime = math.log1p(servercount)# * servercount)# + 3
            print("Sleeping: " + str(int(sleeptime)))
            time.sleep(sleeptime)

    def stop_servers(self):
        for servernumber in range(self.settings.first_server, self.settings.last_server):
            self.stop_server(self.settings.source_image, servernumber)

    def stop_server(self, servername, servernumber):
        print("Stopping server: " + str(servername + str(servernumber)))
        self.server_state = os.system("virsh --connect qemu:///system shutdown clone" + str(servernumber))
        # To avoid starving CPU & IO resources (boot time scale approx. like that)(empirical!)
        if self.server_state is 256:
            self.running_servers = self.running_servers + 1         
        servercount = - (self.settings.first_server - servernumber) - self.running_servers + 1   
	if self.server_state is not 256:
            #sleeptime = math.log(servercount)
            sleeptime = 1
            print("Sleeping: " + str(int(sleeptime)))
            time.sleep(sleeptime)

    def delete_servers(self):
        # TODO: add a warning here: "are you sure?"
        for servernumber in range(self.settings.first_server, self.settings.last_server):
            self.delete_server(self.settings.source_image, servernumber)

    def delete_server(self, servername, servernumber):
        print("Stopping server: " + str(servername + str(servernumber)))
        os.system("virsh --connect qemu:///system undefine clone" + str(servernumber))
        # TODO delete image files (owned by root on Debian!?)

    def destroy_servers(self):
        """ The equivalent of ripping the power cord out of the physical machines."""
        for servernumber in range(self.settings.first_server, self.settings.last_server):
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

    def print_info(self):
        print("First server: " + str(self.settings.first_server))
        print("Number of servers: " + str(self.settings.number_of_servers))
        print("Last server: " + str(self.settings.last_server))

    def create_ip_list(self):
        pass

    def create_server_info(self):
        """ Print number of running server and other stats"""
        pass
