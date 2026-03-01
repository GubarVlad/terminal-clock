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
    canvas_size = size*2 + 1
    while True:
        clear()
        t = time.localtime()
        hour = t.tm_hour % 12
        minute = t.tm_min
        second = t.tm_sec

        canvas = [[' ' for _ in range(canvas_size)] for _ in range(canvas_size)]

        for y in range(canvas_size):
            for x in range(canvas_size):
                dx = x - size
                dy = y - size
                dist = math.sqrt(dx*dx + dy*dy)
                if abs(dist - size) < 0.5:
                    canvas[y][x] = 'o'

        for h in range(1, 13):
            angle = math.pi/2 - 2*math.pi*h/12
            x = size + int(math.cos(angle) * (size - 2))
            y = size - int(math.sin(angle) * (size - 2))
            num_str = str(h)
            for i, ch in enumerate(num_str):
                xi = x - len(num_str)//2 + i
                if 0 <= xi < canvas_size and 0 <= y < canvas_size:
                    canvas[y][xi] = ch

        x0, y0 = size, size
        hour_angle = math.pi/2 - 2*math.pi*(hour + minute/60)/12
        minute_angle = math.pi/2 - 2*math.pi*minute/60
        second_angle = math.pi/2 - 2*math.pi*second/60

        xh = x0 + int(math.cos(hour_angle) * (size*0.5))
        yh = y0 - int(math.sin(hour_angle) * (size*0.5))
        xm = x0 + int(math.cos(minute_angle) * (size*0.8))
        ym = y0 - int(math.sin(minute_angle) * (size*0.8))
        xs = x0 + int(math.cos(second_angle) * (size*0.9))
        ys = y0 - int(math.sin(second_angle) * (size*0.9))

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
