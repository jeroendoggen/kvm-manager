import socket
import sys

HOST = "localhost"
PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto("Hello",(HOST, PORT))

