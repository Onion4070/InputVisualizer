import socket
import struct

class udpsend():
    def __init__(self):
        # 送信元情報
        srcIP = "localhost"
        srcPort = 5005
        self.srcAddr = (srcIP, srcPort)

        # 宛先情報
        dstIP = "localhost"
        dstPort = 7007
        self.dstAddr = (dstIP, dstPort)

        # # ソケット作成
        self.udpClientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.udpClientSock.bind(self.srcAddr)

    def send(self, data):
        self.udpClientSock.sendto(data, self.dstAddr)

    def close(self):
        self.udpClientSock.close()