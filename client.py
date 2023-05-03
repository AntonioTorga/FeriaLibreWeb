import utils
import sys
import socket
import utils as ut

max_size = 16
if len(sys.argv)==3:
    add = (str(sys.argv[1]),int(sys.argv[2]))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

msg = input()
msg = ut.create_tcp_msg(msg)
msg = msg.encode()
client_socket.sendto(msg,add)




