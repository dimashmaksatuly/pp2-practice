import pygame
from clock import Clock

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clock")

clock = pygame.time.Clock()


second_hand = pygame.image.load("/Users/dimash/Desktop/pp2-practice/Practice9/mickeys_clock/images/second.png")
minute_hand = pygame.image.load("/Users/dimash/Desktop/pp2-practice/Practice9/mickeys_clock/images/minute.png")

second_hand = pygame.transform.scale(second_hand, (200, 200))
minute_hand = pygame.transform.scale(minute_hand, (200, 200))

clock_obj = Clock((WIDTH//2, HEIGHT//2), second_hand, minute_hand)

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock_obj.draw(screen)

    pygame.display.flip()
    clock.tick(1)

pygame.quit()