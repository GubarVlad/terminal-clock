import math
import time
import os

RED = '\033[91m'
RESET = '\033[0m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_line(x0, y0, x1, y1, canvas, char, color=''):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        canvas[y0][x0] = f'{color}{char}{RESET}'
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def draw_clock(radius=10):
    size = radius
    while True:
        clear()
        t = time.localtime()
        hour = t.tm_hour % 12
        minute = t.tm_min
        second = t.tm_sec
        canvas = [[' ' for _ in range(size*4+1)] for _ in range(size*2+1)]

        # Циферблат
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

      
        def draw_hand(angle, length, char, color=''):
            x0, y0 = size*2, size
            x1 = x0 + int(length * math.sin(angle) * 2)
            y1 = y0 - int(length * math.cos(angle))
            draw_line(x0, y0, x1, y1, canvas, char, color)

        hour_angle = math.pi/2 - 2*math.pi*(hour + minute/60)/12
        minute_angle = math.pi/2 - 2*math.pi*minute/60
        second_angle = math.pi/2 - 2*math.pi*second/60

        draw_hand(hour_angle, size*0.5, '│')
        draw_hand(minute_angle, size*0.8, '│')
        draw_hand(second_angle, size*0.9, '│', RED)

        canvas[size][size*2] = '+'

        for row in canvas:
            print(''.join(row))
        time.sleep(1)

try:
    draw_clock()
except KeyboardInterrupt:
    clear()
    print("Clock stopped.")
