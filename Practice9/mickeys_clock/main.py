import pygame
from clock import MickeyClock

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

clock = pygame.time.Clock()

image = pygame.image.load("mickeys_clock/images/mickey_hand.png")
image = pygame.transform.scale(image, (200, 200))

mickey = MickeyClock((WIDTH//2, HEIGHT//2), image)

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mickey.draw(screen)

    pygame.display.flip()
    clock.tick(1)

pygame.quit()