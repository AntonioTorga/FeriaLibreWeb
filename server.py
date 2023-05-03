import utils
import socket

buff_size = 16


server_adress = ("localhost", 8000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(server_adress)

while(True):
    msg, add = server_socket.recvfrom(buff_size)
    print(msg)
