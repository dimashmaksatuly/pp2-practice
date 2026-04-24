import random
from settings import *

class Food:
    def __init__(self, snake_body):
        self.position = self.generate(snake_body)

    def generate(self, snake_body):
        while True:
            x = random.randrange(0, WIDTH, BLOCK_SIZE)
            y = random.randrange(0, HEIGHT, BLOCK_SIZE)

            if (x, y) not in snake_body:
                return (x, y)

    def draw(self, screen):
        import pygame
        pygame.draw.rect(screen, (255, 0, 0), (*self.position, BLOCK_SIZE, BLOCK_SIZE))