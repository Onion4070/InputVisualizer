import pygame
import udpsend

pygame.init()
pygame.joystick.init()
controller = pygame.joystick.Joystick(0)
clock = pygame.time.Clock()
udp = udpsend.UDPSender()

try:
    while True:
        pygame.event.pump()
        # 軸
        axes = [controller.get_axis(i) for i in range(controller.get_numaxes())]
        # ボタン
        buttons = [controller.get_button(i) for i in range(controller.get_numbuttons())]

        for i in range(6):
            print(f'{axes[i]:.1f} ', end='')
        print()
        
        udp.send_controller_data(axes, buttons)
        clock.tick(120)

except KeyboardInterrupt:
    udp.close()