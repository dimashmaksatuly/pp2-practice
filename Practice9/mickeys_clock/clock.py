import pygame
import datetime

class MickeyClock:
    def __init__(self, center, image):
        self.center = center
        self.image = image

    def draw_hand(self, screen, angle):
        rotated = pygame.transform.rotate(self.image, angle)
        rect = rotated.get_rect(center=self.center)
        screen.blit(rotated, rect)

    def draw(self, screen):
        now = datetime.datetime.now()

        seconds = now.second
        minutes = now.minute

        sec_angle = -seconds * 6
        min_angle = -minutes * 6

        self.draw_hand(screen, sec_angle)
        self.draw_hand(screen, min_angle)