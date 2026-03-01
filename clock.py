import math
import time
import os

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

def draw_clock(radius=10):
    size = radius
    while True:
        clear()
        t = time.localtime()
        hour = t.tm_hour % 12
        minute = t.tm_min
        second = t.tm_sec
        canvas = [[' ' for _ in range(size*4+1)] for _ in range(size*2+1)]
        for y in range(-size, size+1):
            for x in range(-size*2, size*2+1):
                dist = math.sqrt((x/2)**2 + y**2)
                if abs(dist - size) < 0.5:
                    canvas[y+size][x+size*2] = 'o'
        for h in range(1, 13):
            angle = math.pi/2 - 2*math.pi*h/12
            x = int(size * 0.8 * math.sin(angle) * 2)
            y = int(size * 0.8 * math.cos(angle))
            num_str = str(h)
            for i, ch in enumerate(num_str):
                canvas[size - y][size*2 + x + i - len(num_str)//2] = ch
        x0, y0 = size*2, size
        hour_angle = math.pi/2 - 2*math.pi*(hour + minute/60)/12
        minute_angle = math.pi/2 - 2*math.pi*minute/60
        second_angle = math.pi/2 - 2*math.pi*second/60
        xh = x0 + int(size*0.5 * math.sin(hour_angle) * 2)
        yh = y0 - int(size*0.5 * math.cos(hour_angle))
        xm = x0 + int(size*0.8 * math.sin(minute_angle) * 2)
        ym = y0 - int(size*0.8 * math.cos(minute_angle))
        xs = x0 + int(size*0.9 * math.sin(second_angle) * 2)
        ys = y0 - int(size*0.9 * math.cos(second_angle))
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
