import socket
import sys
import os

HOST = "192.168.1.95"
PORT = 9999
HOSTNAME = str(os.uname()[1])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(HOSTNAME,(HOST, PORT))

