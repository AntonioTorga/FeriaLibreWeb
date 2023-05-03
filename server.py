import utils as ut
import socket

buff_size = 16
head_size = 16

sck_tcp = ut.SocketTCP()
server_adress = ("localhost", 8000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(server_adress)

while(True):
    msg, add = server_socket.recvfrom(head_size + buff_size)
    msg = sck_tcp.parse_segment(msg.decode())
    print(msg["DATOS"])
