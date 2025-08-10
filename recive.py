import udp

controller = udp.UDPReceiver(srcIP='192.168.0.27', srcPort=7007)
controller.start()

while True:
    print('Axes: ', end='')
    print(f'{controller.AXIS_LX:.4f} {controller.AXIS_LY:.4f} {controller.AXIS_RX:.4f} {controller.AXIS_RY:.4f} ', end='')
    print(controller.ZL, controller.ZR, end='')
    print(' Buttons: ')


