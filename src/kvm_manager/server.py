import SocketServer
import time

class UDPHandler(SocketServer.BaseRequestHandler):
    
    def handle(self):
        data = self.request[0] #.strip()
        ip = self.client_address[0]
        file = open("../../virtual-servers.html", "a")
        file.write(ip)
        file.write("\n")
        file.close()