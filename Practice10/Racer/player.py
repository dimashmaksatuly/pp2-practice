import pygame
from settings import *

class Player:
    def __init__(self):
        self.image = pygame.image.load("/Users/dimash/Desktop/pp2-practice/Practice10/Racer/Assets/car.png")
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.x = WIDTH // 2 - 25
        self.y = HEIGHT - 120
        self.speed = PLAYER_SPEED

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if self.x < 0:
            self.x = 0
        if self.x > WIDTH - 50:
            self.x = WIDTH - 50

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return self.image.get_rect(topleft=(self.x, self.y))