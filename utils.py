import socket
from random import randint

buff_size = 16
head_size = 16
end_of_header = "|||"

class SocketTCP:
    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        direccion_destino = None
        direccion_origen = None
        secuencia = None

    def bind(self, address):
        self.sock.bind(address)
        self.direccion_origen = address

    def connect(self,address):
        self.sock.settimeout(1)
        seq = randint(0,100)
        tcp_message = create_tcp_msg(SYN=1,SEQ=seq)
        self.sock.sendto(tcp_message.encode(),address)
        #manejar error de "TimeoutError"
        message, address = self.sock.recvfrom()
        message = self.parse_segment(message.decode())
        if message["SYN"] == 1 and message["ACK"] == 1 and message["FIN"] == 0 and message["SEQ"]==seq+1 and message["DATOS"]=="":
            tcp_message = create_tcp_msg(ACK=1,SEQ=seq+2)
            self.sock.sendto(tcp_message.encode(),address)
            self.sock.direccion_destino = address


    def accept(self):
        self.sock.settimeout(1)
        #manejar error de "TimeoutError"
        message,address = self.sock.recvfrom()
        message = self.parse_segment(message.decode())
        if message["SYN"] == 1 and message["ACK"] == 0 and message["FIN"] == 0  and message["DATOS"]=="":
            seq = message["SEQ"]
            message = create_tcp_msg(SYN=1,ACK=1,SEQ=seq+1)
            self.sock.sendto(message.encode(),address)
            self.direccion_destino = address


    def parse_segment(self, segment):
        parsed_seg = {}

        index = segment.find("|||")
        parsed_seg["SYN"] = int(segment[:index])
        segment = segment[index+3:]

        index = segment.find("|||")
        parsed_seg["ACK"] = int(segment[:index])
        segment = segment[index+3:]

        index = segment.find("|||")
        parsed_seg["FIN"] = int(segment[:index])
        segment = segment[index+3:]

        index = segment.find("|||")
        parsed_seg["SEQ"] = int(segment[:index])
        segment = segment[index+3:]

        parsed_seg["DATOS"] = segment
        
        return parsed_seg
    def create_segment(self, parsed_seg):
        segment = ""
        segment += str(parsed_seg["SYN"]) + "|||"
        segment += str(parsed_seg["ACK"]) + "|||"
        segment += str(parsed_seg["FIN"]) + "|||"
        segment += str(parsed_seg["SEQ"]) + "|||"
        segment += str(parsed_seg["DATOS"]) 

        return segment
    
def create_tcp_msg(msg="", SYN=0, ACK=0, FIN=0, SEQ=0):
    segment = ""
    segment += str(SYN) + "|||"
    segment += str(ACK) + "|||"
    segment += str(FIN) + "|||"
    segment += str(SEQ) + "|||"
    segment += str(msg) 
    return segment

# TESTING RELATED
# sock = SocketTCP()
# tcpsign = "1|||1|||0|||8|||"
# parsed = sock.parse_segment(tcpsign)
# print(parsed)
# unparsed = sock.create_segment(parsed)
# print(unparsed)
# print(tcpsign==unparsed)