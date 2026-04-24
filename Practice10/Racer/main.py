import pygame
from settings import *
from player import Player
from coin import Coin

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()

player = Player()
coin = Coin()

score = 0
font = pygame.font.SysFont("Verdana", 20)

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.move(keys)

    coin.update()

    if player.get_rect().colliderect(coin.get_rect()):
        score += 1
        coin.reset()

    screen.fill((0, 0, 0))

    player.draw(screen)
    coin.draw(screen)

    text = font.render(f"Coins: {score}", True, (255, 255, 255))
    screen.blit(text, (280, 10))

    pygame.display.flip()

pygame.quit()