import pygame
import math
import datetime

class Clock:
    def __init__(self, center, second_hand, minute_hand):
        self.center = center
        self.second_hand = second_hand
        self.minute_hand = minute_hand

    def draw_hand(self, screen, image, angle):
        rotated = pygame.transform.rotate(image, angle)
        rect = rotated.get_rect(center=self.center)
        screen.blit(rotated, rect)

    def draw(self, screen):
        now = datetime.datetime.now()

        seconds = now.second
        minutes = now.minute

        sec_angle = -seconds * 6
        min_angle = -minutes * 6

        self.draw_hand(screen, self.second_hand, sec_angle)
        self.draw_hand(screen, self.minute_hand, min_angle)