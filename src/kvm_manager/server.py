import SocketServer
import datetime

from reporter import Reporter


class UDPHandler(SocketServer.BaseRequestHandler):
    """ Process incoming UDP packets too aggregate information about virtual servers."""
    first_time = 0
    last_time = 0
    server_list = {}

    def handle(self):
        hostname = self.request[0]
        ip_address = self.client_address[0]
        info_file = open("../../virtual-servers.html", "a")
        info_file.write(ip_address)
        info_file.write("\n")
        info_file.close()
        print(ip_address + ":" + hostname )
        self.save_server_info(ip_address, hostname, 42, 42)

    def save_server_info(self, ip_address, hostname, first_time, last_time):
        self.server_list [ip_address] = hostname
        for key in sorted(self.server_list):
            pass
            #print (key + ":" + self.server_list[key])
            #reporter.update_server_list(self.server_list)

    def print_server_info(self):
        pass

 
