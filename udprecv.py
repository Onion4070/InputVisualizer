import socket
import struct

UDP_IP = "0.0.0.0"
UDP_PORT = 7007
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(0.5)

try:
    while True:
        try:
            data, addr = sock.recvfrom(1024)
        except socket.timeout:
            continue

        # アンパック
        unpacked = struct.unpack('6f16B', data)
        
        axes = unpacked[0:6]
        buttons = unpacked[6:22]
        print('Axes: ', end='')
        for i in range(6):
            print(f'{axes[i]:.4f} ', end='')
        print("Buttons:", buttons)
except KeyboardInterrupt:
    sock.close()
finally:
    sock.close()
