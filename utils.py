import socket
end_of_header = "|||"

class SocketTCP:
    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        direccion_destino = None
        direccion_origen = None
        secuencia = None

    def bind(self, address):
        direccion_origen = address

    def connect(address):
        
        direccion_destino = address


    def accept():
        pass 

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
    
def create_tcp_msg(msg, SYN=0, ACK=0, FIN=0, SEQ=0):
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