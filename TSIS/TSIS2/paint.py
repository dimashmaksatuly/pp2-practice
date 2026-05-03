import pygame
import datetime
from tools import flood_fill, draw_rhombus # Импортируем наши инструменты

# Константы (вместо settings.py)
WIDTH, HEIGHT = 1000, 700
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Pro - TSIS 2")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 24)
base_layer = pygame.Surface((WIDTH, HEIGHT))
base_layer.fill(WHITE)

color = BLACK
mode = "pencil"  
thickness = 2
drawing = False
start_pos = None
last_pos = None
text_pos, text_buffer, typing = None, "", False

running = True
while running:
    screen.blit(base_layer, (0, 0))
    if typing and text_pos:
        screen.blit(font.render(text_buffer + "|", True, color), text_pos)

    curr_mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if mode == "text":
                typing, text_pos, text_buffer = True, event.pos, ""
            else:
                drawing, start_pos, last_pos = True, event.pos, event.pos
                if mode == "fill":
                    flood_fill(base_layer, *start_pos, color, WIDTH, HEIGHT)

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                # Финальная отрисовка на base_layer
                if mode == "line":
                    pygame.draw.line(base_layer, color, start_pos, curr_mouse_pos, thickness)
                elif mode == "rect":
                    x, y = min(start_pos[0], curr_mouse_pos[0]), min(start_pos[1], curr_mouse_pos[1])
                    pygame.draw.rect(base_layer, color, (x, y, abs(start_pos[0]-curr_mouse_pos[0]), abs(start_pos[1]-curr_mouse_pos[1])), thickness)
                elif mode == "circle":
                    rad = int(((curr_mouse_pos[0]-start_pos[0])**2 + (curr_mouse_pos[1]-start_pos[1])**2)**0.5)
                    pygame.draw.circle(base_layer, color, start_pos, rad, thickness)
                elif mode == "square":
                    side = max(abs(start_pos[0]-curr_mouse_pos[0]), abs(start_pos[1]-curr_mouse_pos[1]))
                    pygame.draw.rect(base_layer, color, (start_pos[0], start_pos[1], side, side), thickness)
                elif mode == "rhombus":
                    draw_rhombus(base_layer, color, start_pos, curr_mouse_pos, thickness)
                drawing = False

        if event.type == pygame.KEYDOWN:
            if typing:
                if event.key == pygame.K_RETURN:
                    base_layer.blit(font.render(text_buffer, True, color), text_pos)
                    typing = False
                elif event.key == pygame.K_ESCAPE: typing = False
                elif event.key == pygame.K_BACKSPACE: text_buffer = text_buffer[:-1]
                else: text_buffer += event.unicode
                continue

            # Инструменты
            keys = {pygame.K_p: "pencil", pygame.K_e: "eraser", pygame.K_l: "line", 
                    pygame.K_r: "rect", pygame.K_c: "circle", pygame.K_f: "fill", 
                    pygame.K_t: "text", pygame.K_q: "square", pygame.K_h: "rhombus"}
            if event.key in keys: mode = keys[event.key]

            # Размеры
            if event.key == pygame.K_1: thickness = 2
            elif event.key == pygame.K_2: thickness = 5
            elif event.key == pygame.K_3: thickness = 10

            # Цвета
            elif event.key == pygame.K_z: color = RED
            elif event.key == pygame.K_x: color = GREEN
            elif event.key == pygame.K_v: color = BLUE
            elif event.key == pygame.K_b: color = BLACK

            # Сохранение (Ctrl+S)
            if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                name = datetime.datetime.now().strftime("paint_%Y-%m-%d_%H-%M-%S.png")
                pygame.image.save(base_layer, name)

    if drawing:
        if mode == "pencil":
            pygame.draw.line(base_layer, color, last_pos, curr_mouse_pos, thickness)
            last_pos = curr_mouse_pos
        elif mode == "eraser":
            pygame.draw.line(base_layer, WHITE, last_pos, curr_mouse_pos, thickness * 5)
            last_pos = curr_mouse_pos
        elif mode == "line":
            pygame.draw.line(screen, color, start_pos, curr_mouse_pos, thickness)
        elif mode == "rect":
            x, y = min(start_pos[0], curr_mouse_pos[0]), min(start_pos[1], curr_mouse_pos[1])
            pygame.draw.rect(screen, color, (x, y, abs(start_pos[0]-curr_mouse_pos[0]), abs(start_pos[1]-curr_mouse_pos[1])), thickness)
        elif mode == "circle":
            rad = int(((curr_mouse_pos[0]-start_pos[0])**2 + (curr_mouse_pos[1]-start_pos[1])**2)**0.5)
            pygame.draw.circle(screen, color, start_pos, rad, thickness)
        elif mode == "square":
            side = max(abs(start_pos[0]-curr_mouse_pos[0]), abs(start_pos[1]-curr_mouse_pos[1]))
            pygame.draw.rect(screen, color, (start_pos[0], start_pos[1], side, side), thickness)
        elif mode == "rhombus":
            draw_rhombus(screen, color, start_pos, curr_mouse_pos, thickness)

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()