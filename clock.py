import math
import time
import os
import sys

RED = '\033[91m'
RESET = '\033[0m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_line(canvas, x0, y0, x1, y1, char='│', color=''):
    dx = x1 - x0
    dy = y1 - y0
    steps = max(abs(dx), abs(dy))
    if steps == 0:
        canvas[y0][x0] = f'{color}{char}{RESET}'
        return
    x_inc = dx / steps
    y_inc = dy / steps
    x, y = x0, y0
    for _ in range(steps + 1):
        xi, yi = int(round(x)), int(round(y))
        if 0 <= yi < len(canvas) and 0 <= xi < len(canvas[0]):
            if dx == 0:
                c = '│'
            elif dy == 0:
                c = '─'
            elif (dx > 0 and dy < 0) or (dx < 0 and dy > 0):
                c = '/'
            else:
                c = '\\'
            canvas[yi][xi] = f'{color}{c}{RESET}'
        x += x_inc
        y += y_inc

def draw_square_clock(size=11):
    canvas = [[' ' for _ in range(size)] for _ in range(size)]
    positions = {
        12: (0, size//2),
        3:  (size//2, size-1),
        6:  (size-1, size//2),
        9:  (size//2, 0),
        1:  (size//4, 3*size//4),
        2:  (size//4, size-2),
        4:  (3*size//4, size-2),
        5:  (3*size//4, 3*size//4),
        7:  (3*size//4, size//4),
        8:  (3*size//4, 1),
        10: (size//4,1),
        11: (size//4, size//4),
    }
    for h, (y, x) in positions.items():
        s = str(h)
        canvas[y][x:x+len(s)] = list(s)
    return canvas

def draw_clock(size=11):
    center = size//2
    while True:
        clear()
        canvas = draw_square_clock(size)
        t = time.localtime()
        hour = t.tm_hour % 12
        minute = t.tm_min
        second = t.tm_sec

        # стрелки
        hour_angle = math.pi/2 - 2*math.pi*(hour + minute/60)/12
        minute_angle = math.pi/2 - 2*math.pi*minute/60
        second_angle = math.pi/2 - 2*math.pi*second/60

        hour_len = size//3
        minute_len = size//2
        second_len = size//2

        x0, y0 = center, center

        xh = x0 + int(hour_len * math.cos(hour_angle))
        yh = y0 - int(hour_len * math.sin(hour_angle))
        xm = x0 + int(minute_len * math.cos(minute_angle))
        ym = y0 - int(minute_len * math.sin(minute_angle))
        xs = x0 + int(second_len * math.cos(second_angle))
        ys = y0 - int(second_len * math.sin(second_angle))

        draw_line(canvas, x0, y0, xh, yh)
        draw_line(canvas, x0, y0, xm, ym)
        draw_line(canvas, x0, y0, xs, ys, color=RED)

        canvas[y0][x0] = '+'

        for row in canvas:
            print(''.join(row))
        time.sleep(1)

try:
    draw_clock()
except KeyboardInterrupt:
    clear()
    print("Clock stopped.")
