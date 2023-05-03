import utils
import sys
import socket

max_size = 16
if len(sys.argv)==3:
    add = (str(sys.argv[1]),int(sys.argv[2]))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

msg = input()
msg = msg.encode()
client_socket.sendto(msg,add)




