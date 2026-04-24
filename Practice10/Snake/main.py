import pygame
from settings import *
from snake import Snake
from food import Food

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

snake = Snake()
food = Food(snake.body)

score = 0
level = 1
speed = FPS

font = pygame.font.SysFont("Verdana", 20)

running = True
while running:
    clock.tick(speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction((0, -BLOCK_SIZE))
            elif event.key == pygame.K_DOWN:
                snake.change_direction((0, BLOCK_SIZE))
            elif event.key == pygame.K_LEFT:
                snake.change_direction((-BLOCK_SIZE, 0))
            elif event.key == pygame.K_RIGHT:
                snake.change_direction((BLOCK_SIZE, 0))

    snake.move()

    head = snake.body[0]

    if head == food.position:
        snake.grow = True
        score += 1
        food = Food(snake.body)

        if score % 3 == 0:
            level += 1
            speed += 2

    if (head[0] < 0 or head[0] >= WIDTH or
        head[1] < 0 or head[1] >= HEIGHT or
        snake.check_collision()):
        running = False

    screen.fill((0, 0, 0))
    snake.draw(screen)
    food.draw(screen)

    text = font.render(f"Score: {score}  Level: {level}", True, (255,255,255))
    screen.blit(text, (10, 10))

    pygame.display.flip()

pygame.quit()