import random
import pygame
import time

pygame.init()

BLACK = (0, 0, 0)
RED = (213, 50, 80)
WHITE = (255, 255, 255)
BLUE = (50, 153, 213)
YELLOW = (255, 255, 102)
GREEN = (0, 255, 0)

# Set dimension of the screen
displayScreenWidth = 600
displayScreenHeight = 400

displayScreen = pygame.display.set_mode((displayScreenWidth, displayScreenHeight))
# set title game
pygame.display.set_caption("Snake game use A* algorithm")

clock = pygame.time.Clock()

# set size of snake
snakeBlock = 10
snakeSpeed = 15

fontStyle = pygame.font.SysFont("bahnschrift", 25)
fontScore = pygame.font.SysFont("comicsansms", 35)

def score(score):
    value = fontScore.render("Your Score: " + str(score), True, YELLOW)
    displayScreen.blit(value, [0, 0])

# draw snake
def our_snake(snakeBlock, snakeList):
    for x in snakeList:
        pygame.draw.rect(displayScreen, BLACK, [x[0], x[1], snakeBlock, snakeBlock])

# create message 
def message(msg, color):
    mesg = fontStyle.render(msg, True, color)
    displayScreen.blit(mesg, [displayScreenWidth / 6, displayScreenHeight / 3])

def gameLoop():
    gameOver = False
    gameClose = False

    x1 = displayScreenWidth / 2
    y1 = displayScreenHeight / 2

    x1Change = 0
    y1Change = 0

    snakeList = []
    lengthOfSnake = 1

    foodX = round(random.randrange(0, displayScreenWidth - snakeBlock) / 10.0) * 10.0
    foodY = round(random.randrange(0, displayScreenHeight - snakeBlock) / 10.0) * 10.0

    while not gameOver:

        while gameClose == True:
            displayScreen.fill(BLUE)
            message("You Lost! Press C-Play Again or Q-Quit", RED)
            score(lengthOfSnake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameOver = True
                        gameClose = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1Change = -snakeBlock
                    y1Change = 0
                elif event.key == pygame.K_RIGHT:
                    x1Change = snakeBlock
                    y1Change = 0
                elif event.key == pygame.K_UP:
                    y1Change = -snakeBlock
                    x1Change = 0
                elif event.key == pygame.K_DOWN:
                    y1Change = snakeBlock
                    x1Change = 0

        if x1 >= displayScreenWidth or x1 < 0 or y1 >= displayScreenHeight or y1 < 0:
            gameClose = True

        x1 += x1Change
        y1 += y1Change  
        displayScreen.fill(BLUE)  
        # draw food
        pygame.draw.rect(displayScreen, GREEN, [foodX, foodY, snakeBlock, snakeBlock])

        snakeHead = []
        snakeHead.append(x1)
        snakeHead.append(y1)
        snakeList.append(snakeHead)

        if len(snakeList) > lengthOfSnake:
            del snakeList[0]
        
        for x in snakeList[:-1]:
            if x == snakeHead:
                gameClose = True

        our_snake(snakeBlock, snakeList)
        score(lengthOfSnake - 1)
        # update sceen
        pygame.display.update()

        if x1 == foodX and y1 == foodY:
            foodX = round(random.randrange(0, displayScreenWidth - snakeBlock) / 10.0) * 10.0
            foodY = round(random.randrange(0, displayScreenHeight - snakeBlock) / 10.0) * 10.0
            lengthOfSnake += 1
        clock.tick(snakeSpeed)

    pygame.quit()
    quit()

gameLoop()