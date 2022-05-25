import pygame
import numpy
from Spot import Spot
import random

pygame.init()

GAMEOVER = False
# mau su dung
GRAY = (239, 235, 235)
WHITE = (102, 0, 102)
BLUE = (0, 0, 102)
BLUE_1 = (0, 153, 153)
GREEN = (153, 0, 76)
BLACK = (43, 36, 36)
RED = (102, 102, 0)

# khai bao kich thuoc 
cols = 25
rows = 25 
width = 600
height = 600
wr = width / cols
hr = height / rows
# khai bao huong
direction = 1

screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("Snake Game A*")
clock = pygame.time.Clock()
fontScore = pygame.font.SysFont("comicsansms", 35)

# ham tinh diem so
def score(score):
    value = fontScore.render("Score: " + str(score), True, RED)
    screen.blit(value, [0, 0])

# ve duong di cua ran
def ways(food1, snake1):
    food1.camefrom = []
    for s in snake1:
        s.camefrom = []
#   Khoi tao
    way = []
    openset = [snake1[-1]]
    closedset = []
    dir_array1 = []
    while 1:
        #  trả về spot có spot.f bé nhất
        current1 = min(openset,key=lambda x: x.f)
        # openset = [openset[i] for i in range(len(openset)) if not openset[i] == current1]
        openset = list(filter(lambda x: (not x == current1),openset))
        # Them current1 vao danh sach nhung diem da di qua
        closedset.append(current1)
        for neighbor in current1.neighbors:
            if neighbor not in closedset and not neighbor.obstrucle and neighbor not in snake1:
                tempg = neighbor.g + 1
                if neighbor in openset:
                    if tempg < neighbor.g:
                        neighbor.g = tempg
                else:
                    neighbor.g = tempg
                    openset.append(neighbor)
                    # Ham heuristic
                neighbor.h = numpy.sqrt((neighbor.x - food1.x) * 2) + numpy.sqrt((neighbor.y - food1.y) * 2)
                # ham f
                neighbor.f = neighbor.g + neighbor.h
                # Luu vị trí trước của neighbor
                neighbor.camefrom = current1
        if current1 == food1:
            break
        #  Add hướng đi vào dir_array1
    while current1.camefrom:
        way.append(current1)
        current1 = current1.camefrom
    #print(dir_array1)
    # reset lai tat ca cac diem
    for i in range(rows):
        for j in range(cols):
            grid[i][j].camefrom = []
            grid[i][j].f = 0
            grid[i][j].h = 0
            grid[i][j].g = 0
    return way

# lay huong di cua ran
def getpath(food1, snake1):
    food1.camefrom = []
    for s in snake1:
        s.camefrom = []
#   Khoi tao
    openset = [snake1[-1]]
    closedset = []
    dir_array1 = []
    while 1:
        #  trả về spot có spot.f bé nhất
        current1 = min(openset,key=lambda x: x.f)

        # openset = [openset[i] for i in range(len(openset)) if not openset[i] == current1]
        openset = list(filter(lambda x: (not x == current1),openset))
        # Them current1 vao danh sach nhung diem da di qua
        closedset.append(current1)
        for neighbor in current1.neighbors:
            if neighbor not in closedset and not neighbor.obstrucle and neighbor not in snake1:
                tempg = neighbor.g + 1
                if neighbor in openset:
                    if tempg < neighbor.g:
                        neighbor.g = tempg
                else:
                    neighbor.g = tempg
                    openset.append(neighbor)
                    # Ham heuristic
                neighbor.h = numpy.sqrt((neighbor.x - food1.x) * 2) + numpy.sqrt((neighbor.y - food1.y) * 2)
                # ham f
                neighbor.f = neighbor.g + neighbor.h
                # Luu vị trí trước của neighbor
                neighbor.camefrom = current1
        if current1 == food1:
            break
        #  Add hướng đi vào dir_array1
    while current1.camefrom:
        if current1.x == current1.camefrom.x and current1.y < current1.camefrom.y:
            dir_array1.append(2)
        elif current1.x == current1.camefrom.x and current1.y > current1.camefrom.y:
            dir_array1.append(0)
        elif current1.x < current1.camefrom.x and current1.y == current1.camefrom.y:
            dir_array1.append(3)
        elif current1.x > current1.camefrom.x and current1.y == current1.camefrom.y:
            dir_array1.append(1)
        current1 = current1.camefrom
    # reset lai tat ca cac diem
    for i in range(rows):
        for j in range(cols):
            grid[i][j].camefrom = []
            grid[i][j].f = 0
            grid[i][j].h = 0
            grid[i][j].g = 0
    return dir_array1


grid = []
for i in range(rows):
      grid.append([])
      for j in range(cols):
            grid[i].append(Spot(i,j)) 
for i in range(rows):
      for j in range(cols):
            grid[i][j].add_neighbors(grid, rows, cols)

snake = [grid[round(rows/2)][round(cols/2)]]
food = grid[random.randint(0, rows-1)][random.randint(0, cols-1)]
current = snake[-1]
dir_array = getpath(food, snake)
food_array = [food]
way = ways(food, snake)

while not GAMEOVER:
    clock.tick(8)
    screen.fill(GRAY)
    direction = dir_array.pop(-1)
    score(len(food_array) - 1)
    if way:
        way.pop(-1)
    for spot in way:
        spot.show(BLUE_1, hr, wr, screen)

    if direction == 0:    # down
        snake.append(grid[current.x][current.y + 1])
    elif direction == 1:  # right
        snake.append(grid[current.x + 1][current.y])
    elif direction == 2:  # up
        snake.append(grid[current.x][current.y - 1])
    elif direction == 3:  # left
        snake.append(grid[current.x - 1][current.y])
    current = snake[-1]

    if current.x == food.x and current.y == food.y:
        while 1:
            food = grid[random.randint(0, rows - 1)][random.randint(0, cols - 1)]
            if not (food.obstrucle or food in snake):
                break
        food_array.append(food)
        dir_array = getpath(food, snake)
        way = ways(food, snake)

    else:
        snake.pop(0)

    for spot in snake:
        spot.show(WHITE, hr, wr, screen)

    for i in range(rows):
        for j in range(cols):
            if grid[i][j].obstrucle:
                grid[i][j].show(BLACK, hr, wr, screen)

    food.show(GREEN, hr, wr, screen)
    snake[-1].show(BLUE, hr, wr, screen)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAMEOVER = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and not direction == 0:
                direction = 2
            elif event.key == pygame.K_a and not direction == 1:
                direction = 3
            elif event.key == pygame.K_s and not direction == 2:
                direction = 0
            elif event.key == pygame.K_d and not direction == 3:
                direction = 1