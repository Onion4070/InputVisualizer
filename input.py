import pygame
from pygame.locals import *
import platform
from typing import Tuple
from pygame import gfxdraw

WIDTH  = 660
HEIGHT = 440

L_CENTER = (173, 155)
R_CENTER = (403, 227)

BACKGROUND = (230, 230, 230)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
OFF_WHITE = (238, 238, 238)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

CONTROLLER_IMG_PATH = './img/test.png'
L_IMG_PATH = './img/L.png'
R_IMG_PATH = './img/R.png'

COORD_A = (515, 139)
COORD_B = (472, 177)
COORD_X = (472, 100)
COORD_Y = (428, 139)

CENTER_A = (521, 153)
CENTER_B = (478, 191)
CENTER_X = (478, 115)
CENTER_Y = (434, 153)

os_name = platform.system()


# 単純移動平均
def moving_average(axis_x: float, axis_y: float, history_x: list, history_y: list) -> Tuple[int, int]:
    window_size = 4
    deadzone = 0.02

    history_x.append(axis_x)
    history_y.append(axis_y)

    if len(history_y) < window_size:
        return 0, 0
    
    avg_x = sum(history_x) / window_size
    avg_y = sum(history_y) / window_size
    history_x.pop(0)
    history_y.pop(0)

    # 円形デッドゾーン
    if axis_x**2 + axis_y**2 <= deadzone:
        return 0, 0
    return int(25*avg_x), int(25*avg_y)


def draw_stick(screen, center_coord: tuple, offset: tuple, press: bool) -> None:
    x, y = center_coord
    dx, dy = offset
    # アンチエイリアシングして描画
    ## スティック縁線
    gfxdraw.aacircle(screen, x+dx, y+dy, 31, BLACK)

    ## スティック
    if press:
        draw_filled_aacircle(screen, (x+dx, y+dy), 30, RED)
    else:
        draw_filled_aacircle(screen, (x+dx, y+dy), 30, OFF_WHITE)


    ## スティック内側の溝
    gfxdraw.aacircle(screen, int(x+dx*1.2), int(y+dy*1.2), 24, BLACK)


def draw_filled_aacircle(screen, center_coord: tuple, radius: int, ColorValue: tuple) -> None:
    x = center_coord[0]
    y = center_coord[1]

    gfxdraw.filled_circle(screen, x, y, radius, ColorValue)
    gfxdraw.aacircle(screen, x, y, radius, ColorValue)


def main() -> None:
    pygame.init()
    pygame.joystick.init()
    controller = pygame.joystick.Joystick(0)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    controller_img = pygame.image.load(CONTROLLER_IMG_PATH).convert_alpha()
    l_img = pygame.image.load(L_IMG_PATH).convert_alpha()
    r_img = pygame.image.load(R_IMG_PATH).convert_alpha()

    history_lx, history_ly = [], []
    history_rx, history_ry = [], []
    running = True

    # フォント, テキスト設定
    font = pygame.font.SysFont('meiryo', 20)
    textA = font.render('A', True, WHITE)
    textB = font.render('B', True, WHITE)
    textX = font.render('X', True, WHITE)
    textY = font.render('Y', True, WHITE)

    while (running):
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            
            # マウス座標取得(開発用)
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                print(f'pos = {mouse_pos}')

        # コントローラ情報の取得
        axes = [controller.get_axis(i) for i in range(controller.get_numaxes())]
        buttons = [controller.get_button(i) for i in range(controller.get_numbuttons())]

        # スティック位置を取得
        Lstick_offset = moving_average(axes[0], axes[1], history_lx, history_ly)
        Rstick_offset = moving_average(axes[2], axes[3], history_rx, history_ry)

        # 生データ(LRスティック)
        rawL = controller.get_axis(0), controller.get_axis(1)
        rawR = controller.get_axis(2), controller.get_axis(3)
        # print(f'{rawL[0]:.4f} {rawL[1]:.4f} {rawR[0]:.4f} {rawR[1]:.4f}')

        screen.fill(GREEN)
        screen.blit(controller_img, (0, 0))

        # ボタンの押下状況に応じて色を変化
        ## ABXY
        if buttons[0]:
            draw_filled_aacircle(screen, CENTER_A, 20, RED)
        if buttons[1]:
            draw_filled_aacircle(screen, CENTER_B, 20, RED)
        if buttons[2]:
            draw_filled_aacircle(screen, CENTER_X, 20, RED)
        if buttons[3]:
            draw_filled_aacircle(screen, CENTER_Y, 20, RED)

        ## -HOME+

        # スティック描画
        ## LD, RD
        draw_stick(screen, L_CENTER, Lstick_offset, buttons[7])
        draw_stick(screen, R_CENTER, Rstick_offset, buttons[8])

        ## LR
        if buttons[9]:
            screen.blit(l_img, (0, 0))

        if buttons[10]:
            screen.blit(r_img, (0, 0))


        screen.blit(textA, COORD_A)
        screen.blit(textB, COORD_B)
        screen.blit(textY, COORD_Y)
        screen.blit(textX, COORD_X)



        # pygameのイベント更新(これがないとスティック位置が更新されない)
        pygame.event.pump()
        pygame.display.flip()
        # pygame.display.update()
        clock.tick(120)
    pygame.quit()

if __name__ == '__main__':
    main()