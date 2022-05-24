from pygame import display, time, draw, QUIT, init, KEYDOWN, K_a, K_s, K_d, K_w
from random import randint
import pygame
from numpy import sqrt
import time as pe
init()

done = False
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 102)

cols = 25
rows = 25 

width = 600
height = 600
wr = width/cols
hr = height/rows
direction = 1

screen = display.set_mode([width, height])
display.set_caption("snake_self")
clock = time.Clock()
fontScore = pygame.font.SysFont("comicsansms", 35)

def score(score):
    value = fontScore.render("Your Score: " + str(score), True, YELLOW)
    screen.blit(value, [0, 0])
class Spot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.camefrom = []
        self.obstrucle = False
        if randint(1, 101) < 3:
            self.obstrucle = True

    def show(self, color):
        draw.rect(screen, color, [self.x*hr+2, self.y*wr+2, hr-4, wr-4])

    def add_neighbors(self):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.x < rows - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y < cols - 1:
            self.neighbors.append(grid[self.x][self.y + 1])
    def __str__(self) -> str:
        return str(self.y) + " " +str(self.y)

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
                neighbor.h = sqrt((neighbor.x - food1.x) * 2) + sqrt((neighbor.y - food1.y) * 2)
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
                neighbor.h = sqrt((neighbor.x - food1.x) * 2) + sqrt((neighbor.y - food1.y) * 2)
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




#  sua lai doan nay
# khoi tao cac diem
# grid = [[Spot(i, j) for j in range(cols)] for i in range(rows)]
grid = []
for i in range(rows):
    grid.append([])
    for j in range(cols):
        grid[i].append(Spot(i,j)) 
for i in range(rows):
    for j in range(cols):
        grid[i][j].add_neighbors()

snake = [grid[round(rows/2)][round(cols/2)]]
food = grid[randint(0, rows-1)][randint(0, cols-1)]
current = snake[-1]
dir_array = getpath(food, snake)
food_array = [food]
way = ways(food, snake)

while not done:
    clock.tick(8)
    screen.fill(BLACK)
    direction = dir_array.pop(-1)
    score(len(food_array) - 1)
    if way:
        way.pop(-1)
    for spot in way:
        spot.show(YELLOW)

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
            food = grid[randint(0, rows - 1)][randint(0, cols - 1)]
            if not (food.obstrucle or food in snake):
                break
        food_array.append(food)
        dir_array = getpath(food, snake)
        way = ways(food, snake)

            
    else:
        snake.pop(0)

    for spot in snake:
        spot.show(WHITE)

    for i in range(rows):
        for j in range(cols):
            if grid[i][j].obstrucle:
                grid[i][j].show(RED)

    food.show(GREEN)
    snake[-1].show(BLUE)
    display.flip()
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == KEYDOWN:
            if event.key == K_w and not direction == 0:
                direction = 2
            elif event.key == K_a and not direction == 1:
                direction = 3
            elif event.key == K_s and not direction == 2:
                direction = 0
            elif event.key == K_d and not direction == 3:
                direction = 1