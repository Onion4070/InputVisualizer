import pygame
from pygame.locals import *
import sys
from typing import Tuple

WIDTH  = 400
HEIGHT = 300

L_CENTER = (100, 150)
R_CENTER = (300, 150)

BACKGROUND = (230, 230, 230)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GLAY = (192, 192, 192)
GREEN = (0, 255, 0)


def init() -> None:
    pygame.init()
    pygame.joystick.init()


# 単純移動平均
def moving_average(axis_x: float, axis_y: float, history_x: list, history_y: list) -> Tuple[int, int]:
    window_size = 4
    deadzone = 0.02

    history_x.append(axis_x)
    history_y.append(axis_y)

    if len(history_y) < window_size:
        return 0, 0
    
    mean_x = sum(history_x) / window_size
    mean_y = sum(history_y) / window_size
    history_x.pop(0)
    history_y.pop(0)

    # 円形デッドゾーン
    if axis_x**2 + axis_y**2 <= deadzone:
        return 0, 0
    
    return int(25*mean_x), int(25*mean_y)


def draw_stick(screen, center_coord: tuple, offset: tuple) -> None:
    x, y = center_coord
    dx, dy = offset
    pygame.draw.circle(screen, GLAY, center_coord, 55, 1)
    pygame.draw.circle(screen, GLAY, (x+dx, y+dy), 30, 2)
    pygame.draw.circle(screen, BLACK, (x+dx, y+dy), 30)
    pygame.draw.circle(screen, GLAY, (x+dx*1.15, y+dy*1.15), 24, 1)


def main() -> None:
    init()
    controller = pygame.joystick.Joystick(0)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    history_lx, history_ly = [], []
    history_rx, history_ry = [], []

    while (True):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # スティック位置を取得
        Lstick_offset = moving_average(controller.get_axis(0), controller.get_axis(1), history_lx, history_ly)
        Rstick_offset = moving_average(controller.get_axis(2), controller.get_axis(3), history_rx, history_ry)

        # 生データ(Lスティック)
        rawL = controller.get_axis(0), controller.get_axis(1)
        print(rawL)

        screen.fill(WHITE)

        # スティック描画(簡易モデル)
        draw_stick(screen, L_CENTER, Lstick_offset)
        draw_stick(screen, R_CENTER, Rstick_offset)

        # pygameのイベント更新(これがないとスティック位置が更新されない)
        pygame.event.pump()
        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()