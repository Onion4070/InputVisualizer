import pygame
import udpsend
import struct

pygame.init()
pygame.joystick.init()
controller = pygame.joystick.Joystick(0)
clock = pygame.time.Clock()
udp = udpsend.udpsend()

try:
    while True:
        pygame.event.pump()
        # 軸
        axes = [controller.get_axis(i) for i in range(controller.get_numaxes())]
        # ボタン
        buttons = [controller.get_button(i) for i in range(controller.get_numbuttons())]
        # ハット（方向パッド）
        hats = [controller.get_hat(i) for i in range(controller.get_numhats())]

        for i in range(6):
            print(f'{axes[i]:.1f} ', end='')
        print()
        
        # 軸6個 + ボタン16個
        # 'f'->float, 'B'->unsigned charでpack
        data = struct.pack(
            '6f16B',
            *axes[:6],
            *buttons[:16],
        )
        udp.send(data)
        clock.tick(120)

except KeyboardInterrupt:
    udp.close()