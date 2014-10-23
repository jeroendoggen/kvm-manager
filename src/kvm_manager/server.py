import SocketServer
import os

from datetime import datetime
from reporter import Reporter


class UDPHandler(SocketServer.BaseRequestHandler):
    """ Process incoming UDP packets too aggregate information about virtual servers."""
    first_time = 0
    last_time = 0
    server_list = {}

    def handle(self):
        hostname = self.request[0]
        ip_address = self.client_address[0]
        self.save_server_info(ip_address, hostname, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def save_server_info(self, ip_address, hostname, last_time):
        self.server_list [ip_address] = hostname + " : " + str(last_time)
        for key in sorted(self.server_list):
            # TODO check the payload (check if it is a valid hostname)
            print (key + ":" + self.server_list[key])
            self.write_summary()

    def write_summary(self):
        """ Write a summary of the server info to a logfile """
        try:
            #os.chdir(self.settings.output_path)
            outfile = open("servers.txt", 'w+')
            outfile.write("IP Address : Hostname : Last seen on\n")
            outfile.write("------------------------------------\n")
            outfile.write(str(self.server_list))
            outfile.close()
            with open("servers.txt") as f:
                content = f.read()
                print(content)
            outfile.close()
        except OSError:
            self.exit_program("writing the summary")

    def exit_program(self, message):
        """ Exit the program with an error message
           TODO: this should move somewhere else (needed in multiple places)
        """
        print("Error while " + message)
        print("Closing application")
        sys.exit()

 
