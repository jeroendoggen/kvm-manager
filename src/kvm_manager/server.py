import SocketServer


class UDPHandler(SocketServer.BaseRequestHandler):
    """ Process incoming UDP packets too aggregate information about virtual servers."""

    def handle(self):
        data = self.request[0]
        server_ip = self.client_address[0]
        info_file = open("../../virtual-servers.html", "a")
        info_file.write(server_ip)
        info_file.write("\n")
        info_file.close()
