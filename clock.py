import math
import time
import os
import sys
import shutil

RED = '\033[91m'
RESET = '\033[0m'
CLEAR_SCREEN = '\033[2J'
HOME = '\033[H'
HIDE_CURSOR = '\033[?25l'
SHOW_CURSOR = '\033[?25h'
ALT_SCREEN_ON = '\033[?1049h'
ALT_SCREEN_OFF = '\033[?1049l'
SET_TITLE = '\033]0;terminal-clock\007'

def clear():
    sys.stdout.write(CLEAR_SCREEN + HOME)
    sys.stdout.flush()

def init_terminal():
    sys.stdout.write(SET_TITLE + ALT_SCREEN_ON + CLEAR_SCREEN + HOME + HIDE_CURSOR)
    sys.stdout.flush()

def restore_terminal():
    sys.stdout.write(SHOW_CURSOR + ALT_SCREEN_OFF)
    sys.stdout.flush()

def resize_terminal(cols, rows):
    sys.stdout.write(f'\033[8;{rows};{cols}t')
    sys.stdout.flush()

def get_terminal_size():
    try:
        size = shutil.get_terminal_size()
        return size.columns, size.lines
    except:
        return 80, 24

def check_terminal_size(required_width, required_height):
    cols, lines = get_terminal_size()
    if cols < required_width or lines < required_height:
        sys.stdout.write(CLEAR_SCREEN + HOME + SHOW_CURSOR)
        print(f"Error: Terminal too small!")
        print(f"Required: {required_width} columns × {required_height} lines")
        print(f"Current:  {cols} columns × {lines} lines")
        print(f"\nPlease resize your terminal and try again.")
        sys.exit(1)

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
    width = size * 2
    canvas = [[' ' for _ in range(width)] for _ in range(size)]
    
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
    
    positions = {
        12: (1, width//2-1),
        1:  (3, width-6),
        2:  (6, width-4),
        3:  (size//2, width-3),
        4:  (size-7, width-4),
        5:  (size-4, width-6),
        6:  (size-2, width//2),
        7:  (size-4, 4),
        8:  (size-7, 2),
        9:  (size//2, 1),
        10: (6, 1),
        11: (3, 3),
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
    required_height = size + 1
    required_width = width
    
    check_terminal_size(required_width, required_height)
    resize_terminal(required_width, required_height)
    init_terminal()
    
    try:
        while True:
            cols, lines = get_terminal_size()
            if cols < required_width or lines < required_height:
                restore_terminal()
                print("\nTerminal resized too small. Exiting.")
                break
            
            clear()
            canvas = draw_square_clock(size)
            t = time.localtime()
            hour = t.tm_hour % 12
            minute = t.tm_min
            second = t.tm_sec

            hour_angle = math.pi/2 - 2*math.pi*(hour + minute/60)/12
            minute_angle = math.pi/2 - 2*math.pi*minute/60
            second_angle = math.pi/2 - 2*math.pi*second/60

            hour_len = size // 3
            minute_len = (size // 2) - 1
            second_len = (size // 2) - 1

            xh = center_x + int(hour_len * 2 * math.cos(hour_angle))
            yh = center_y - int(hour_len * math.sin(hour_angle))
            xm = center_x + int(minute_len * 2 * math.cos(minute_angle))
            ym = center_y - int(minute_len * math.sin(minute_angle))
            xs = center_x + int(second_len * 2 * math.cos(second_angle))
            ys = center_y - int(second_len * math.sin(second_angle))

            draw_line(canvas, center_x, center_y, xh, yh)
            draw_line(canvas, center_x, center_y, xm, ym)
            draw_line(canvas, center_x, center_y, xs, ys, color=RED)

            canvas[center_y][center_x] = '+'

            for row in canvas:
                sys.stdout.write(''.join(row) + '\n')
            
            copyright_text = '© vladgubar, 2026'
            padding = (width - len(copyright_text)) // 2
            sys.stdout.write(' ' * padding + copyright_text + '\n')
            sys.stdout.flush()
            time.sleep(1)
    finally:
        restore_terminal()

if __name__ == '__main__':
    try:
        draw_clock()
    except KeyboardInterrupt:
        restore_terminal()
        print("\nClock stopped.")
