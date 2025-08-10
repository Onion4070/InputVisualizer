import socket
import struct
import threading


class UDPSender():
    def __init__(self, dstIP='localhost', dstPort=7007):
        # 宛先情報
        self.dstAddr = (dstIP, dstPort)

        # ソケット作成
        self.udpClientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_controller_data(self, axes, buttons):
        # 軸6個 + ボタン16個
        # 'f'->float, 'B'->unsigned charでpack
        data = struct.pack('6f16B', *axes[:6], *buttons[:16])
        self.udpClientSock.sendto(data, self.dstAddr)

    def close(self):
        self.udpClientSock.close()


class UDPReceiver:
    def __init__(self, srcIP='localhost', srcPort=7007):
        self.srcAddr = (srcIP, srcPort)

        self.BUFSIZE = 1024
        self.udpServerSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # ソケット作成
        self.udpServerSock.bind(self.srcAddr)
        self.udpServerSock.settimeout(0.5)

        self.running = False

        # 初期化
        self.reset_state()

    def reset_state(self):
        self.A = 0
        self.B = 0
        self.X = 0
        self.Y = 0
        self.MINUS = 0
        self.HOME = 0
        self.PLUS = 0
        self.LD = 0
        self.RD = 0
        self.L = 0
        self.R = 0
        self.DPAD_UP = 0
        self.DPAD_DOWN = 0
        self.DPAD_LEFT = 0
        self.DPAD_RIGHT = 0
        self.CAPTURE = 0

        self.AXIS_LX = 0.0
        self.AXIS_LY = 0.0
        self.AXIS_RX = 0.0
        self.AXIS_RY = 0.0
        self.ZL = 0
        self.ZR = 0

    def receive_loop(self):
        while self.running:
            try:
                data, addr = self.udpServerSock.recvfrom(self.BUFSIZE)
                unpacked = struct.unpack('4f16B', data)
                
                axes = unpacked[0:4]
                buttons = unpacked[4:18]

                # ボタン
                self.A = buttons[0]
                self.B = buttons[1]
                self.X = buttons[2]
                self.Y = buttons[3]
                self.MINUS = buttons[4]
                self.HOME = buttons[5]
                self.PLUS = buttons[6]
                self.LD = buttons[7]
                self.RD = buttons[8]
                self.L = buttons[9]
                self.R = buttons[10]
                self.DPAD_UP = buttons[11]
                self.DPAD_DOWN = buttons[12]
                self.DPAD_LEFT = buttons[13]
                self.DPAD_RIGHT = buttons[14]
                self.CAPTURE = buttons[15]

                # 軸
                self.AXIS_LX = axes[0]
                self.AXIS_LY = axes[1]
                self.AXIS_RX = axes[2]
                self.AXIS_RY = axes[3]
                self.ZL = 1 if axes[4] > 0.5 else 0
                self.ZR = 1 if axes[5] > 0.5 else 0

            except socket.timeout:
                continue
            except OSError:
                break

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.receive_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        self.udpServerSock.close()
        if hasattr(self, "thread"):
            self.thread.join()
