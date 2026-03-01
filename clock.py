import math
import time
import os
import sys

RED = '\033[91m'
RESET = '\033[0m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def angle_to_coord(angle, radius):
    x = int(radius * math.sin(angle))
    y = int(radius * math.cos(angle))
    return x, y

def draw_clock(hour, minute, second, radius=10):
    size = radius
    canvas = [[' ' for _ in range(size*4+1)] for _ in range(size*2+1)]
    for y in range(-size, size+1):
        for x in range(-size*2, size*2+1):
            dist = math.sqrt((x/2)**2 + y**2)
            if abs(dist - size) < 0.7:
                canvas[y+size][x+size*2] = 'o'
    hour_angle = math.pi/2 - 2*math.pi*(hour % 12)/12 - math.pi/360*minute
    hx, hy = angle_to_coord(hour_angle, size*0.5)
    canvas[size-hy][size*2+hx] = 'H'
    min_angle = math.pi/2 - 2*math.pi*minute/60
    mx, my = angle_to_coord(min_angle, size*0.8)
    canvas[size-my][size*2+mx] = 'M'
    sec_angle = math.pi/2 - 2*math.pi*second/60
    sx, sy = angle_to_coord(sec_angle, size*0.9)
    canvas[size-sy][size*2+sx] = f'{RED}S{RESET}'
    canvas[size][size*2] = '+'
    for row in canvas:
        print(''.join(row))

def main():
    try:
        while True:
            clear()
            t = time.localtime()
            draw_clock(t.tm_hour, t.tm_min, t.tm_sec)
            time.sleep(1)
    except KeyboardInterrupt:
        clear()
        print("Clock stopped.")

if __name__ == "__main__":
    main()
