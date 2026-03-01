import math
import time
import os
import sys

RED = '\033[91m'
RESET = '\033[0m'
CLEAR_SCREEN = '\033[2J'
HOME = '\033[H'
HIDE_CURSOR = '\033[?25l'
SHOW_CURSOR = '\033[?25h'

def clear():
    sys.stdout.write(HOME)
    sys.stdout.flush()

def init_terminal():
    sys.stdout.write(CLEAR_SCREEN + HOME + HIDE_CURSOR)
    sys.stdout.flush()

def restore_terminal():
    sys.stdout.write(SHOW_CURSOR + '\n')
    sys.stdout.flush()

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

def draw_square_clock(size=21):
    # Double width to make it visually square (terminal chars are ~2:1 ratio)
    width = size * 2
    canvas = [[' ' for _ in range(width)] for _ in range(size)]
    
    # Draw square border
    for i in range(width):
        canvas[0][i] = '─'
        canvas[size-1][i] = '─'
    for i in range(size):
        canvas[i][0] = '│'
        canvas[i][width-1] = '│'
    canvas[0][0] = '┌'
    canvas[0][width-1] = '┐'
    canvas[size-1][0] = '└'
    canvas[size-1][width-1] = '┘'
    
    # Position numbers evenly around the square
    positions = {
        12: (1, width//2-1),          # top center
        1:  (3, width-6),             # top right
        2:  (6, width-4),             # right upper
        3:  (size//2, width-3),       # right center
        4:  (size-7, width-4),        # right lower
        5:  (size-4, width-6),        # bottom right
        6:  (size-2, width//2),       # bottom center
        7:  (size-4, 4),              # bottom left
        8:  (size-7, 2),              # left lower
        9:  (size//2, 1),             # left center
        10: (6, 1),                   # left upper
        11: (3, 3),                   # top left
    }
    for h, (y, x) in positions.items():
        s = str(h)
        for i, c in enumerate(s):
            if 0 <= y < size and 0 <= x+i < width:
                canvas[y][x+i] = c
    return canvas

def draw_clock(size=21):
    width = size * 2
    center_x = width // 2
    center_y = size // 2
    
    init_terminal()
    
    try:
        while True:
            clear()
            canvas = draw_square_clock(size)
            t = time.localtime()
            hour = t.tm_hour % 12
            minute = t.tm_min
            second = t.tm_sec

            # Clock hands angles
            hour_angle = math.pi/2 - 2*math.pi*(hour + minute/60)/12
            minute_angle = math.pi/2 - 2*math.pi*minute/60
            second_angle = math.pi/2 - 2*math.pi*second/60

            # Hand lengths - adjusted for double width
            hour_len = size // 3
            minute_len = (size // 2) - 1
            second_len = (size // 2) - 1

            # Calculate hand endpoints
            xh = center_x + int(hour_len * 2 * math.cos(hour_angle))
            yh = center_y - int(hour_len * math.sin(hour_angle))
            xm = center_x + int(minute_len * 2 * math.cos(minute_angle))
            ym = center_y - int(minute_len * math.sin(minute_angle))
            xs = center_x + int(second_len * 2 * math.cos(second_angle))
            ys = center_y - int(second_len * math.sin(second_angle))

            # Draw hands
            draw_line(canvas, center_x, center_y, xh, yh)
            draw_line(canvas, center_x, center_y, xm, ym)
            draw_line(canvas, center_x, center_y, xs, ys, color=RED)

            canvas[center_y][center_x] = '+'

            # Render with fixed dimensions
            for row in canvas:
                sys.stdout.write(''.join(row) + '\n')
            sys.stdout.flush()
            time.sleep(1)
    finally:
        restore_terminal()

if __name__ == '__main__':
    try:
        draw_clock()
    except KeyboardInterrupt:
        restore_terminal()
        print("Clock stopped.")
