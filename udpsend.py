import socket
import struct

class UDPSender():
    def __init__(self):
        # 送信元情報
        srcIP = "localhost"
        srcPort = 5005
        self.srcAddr = (srcIP, srcPort)

        # 宛先情報
        dstIP = "localhost"
        dstPort = 7007
        self.dstAddr = (dstIP, dstPort)

        # ソケット作成
        self.udpClientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpClientSock.bind(self.srcAddr)

    def send_controller_data(self, axes, buttons):
        # 軸6個 + ボタン16個
        # 'f'->float, 'B'->unsigned charでpack
        data = struct.pack('6f16B', *axes[:6], *buttons[:16])
        self.udpClientSock.sendto(data, self.dstAddr)

    def close(self):
        self.udpClientSock.close()