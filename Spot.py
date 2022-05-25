import pygame
import random

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
            if random.randint(1, 101) < 3:
                  self.obstrucle = True

      def show(self, color, hr, wr, screen):
            pygame.draw.rect(screen, color, [self.x*hr+2, self.y*wr+2, hr-4, wr-4])

      def add_neighbors(self, grid, rows, cols):
            if self.x > 0:
                  self.neighbors.append(grid[self.x - 1][self.y])
            if self.y > 0:
                  self.neighbors.append(grid[self.x][self.y - 1])
            if self.x < rows - 1:
                  self.neighbors.append(grid[self.x + 1][self.y])
            if self.y < cols - 1:
                  self.neighbors.append(grid[self.x][self.y + 1])
                  
      def __str__(self):
            return str(self.y) + " " +str(self.y)