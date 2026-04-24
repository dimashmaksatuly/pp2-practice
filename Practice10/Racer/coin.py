import pygame
import random
from settings import *

class Coin:
    def __init__(self):
        self.image = pygame.image.load("/Users/dimash/Desktop/pp2-practice/Practice10/Racer/Assets/coin.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.reset()

    def reset(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = -100

    def update(self):
        self.y += COIN_SPEED
        if self.y > HEIGHT:
            self.reset()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return self.image.get_rect(topleft=(self.x, self.y))