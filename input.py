import pygame
from pygame.locals import *
import sys

WIDTH  = 400
HEIGHT = 300

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GLAY = (192, 192, 192)

def init() -> None:
    pygame.init()
    pygame.joystick.init()

def main() -> None:
    init()
    controller = pygame.joystick.Joystick(0)
    clock = pygame.time.Clock()

    while (True):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # スティック位置を取得
        Lstick_offset = controller.get_axis(0), controller.get_axis(1)
        Rstick_offset = controller.get_axis(2), controller.get_axis(3)

        print(Lstick_offset)
        # pygameのイベント更新(これがないとスティック位置が更新されない)
        pygame.event.pump()
        clock.tick(60)

if __name__ == '__main__':
    main()
