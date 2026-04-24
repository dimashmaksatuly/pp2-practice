import pygame
from settings import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

color = BLACK
mode = "brush"  

drawing = False
start_pos = None

screen.fill(WHITE)

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            if mode == "rect":
                x = min(start_pos[0], end_pos[0])
                y = min(start_pos[1], end_pos[1])
                w = abs(start_pos[0] - end_pos[0])
                h = abs(start_pos[1] - end_pos[1])

                pygame.draw.rect(screen, color, (x, y, w, h), 2)

            elif mode == "circle":
                radius = int(((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2)**0.5)
                pygame.draw.circle(screen, color, start_pos, radius, 2)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                mode = "brush"
            elif event.key == pygame.K_2:
                mode = "rect"
            elif event.key == pygame.K_3:
                mode = "circle"
            elif event.key == pygame.K_4:
                mode = "eraser"

            elif event.key == pygame.K_r:
                color = RED
            elif event.key == pygame.K_g:
                color = GREEN
            elif event.key == pygame.K_b:
                color = BLUE
            elif event.key == pygame.K_k:
                color = BLACK

    if drawing:
        mouse_pos = pygame.mouse.get_pos()

        if mode == "brush":
            pygame.draw.circle(screen, color, mouse_pos, 5)

        elif mode == "eraser":
            pygame.draw.circle(screen, WHITE, mouse_pos, 10)

    pygame.display.flip()

pygame.quit()