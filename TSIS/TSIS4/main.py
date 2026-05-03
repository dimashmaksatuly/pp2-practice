import pygame
import sys
import random
from db import init_db, save_game_result, get_leaderboard, get_personal_best
from config import load_settings, save_settings
from game import Game, WIDTH, HEIGHT, CELL_SIZE

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Pro: TSIS 4")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 24)

# Создаем таблицы в БД, если их еще нет
init_db()

def draw_text(text, x, y, color=(255, 255, 255), center=False):
    surf = font.render(str(text), True, color)
    rect = surf.get_rect(center=(x, y) if center else (x, y))
    screen.blit(surf, rect)

def menu_screen():
    """Главное меню с вводом имени"""
    username = ""
    settings = load_settings()
    while True:
        screen.fill((20, 20, 30))
        draw_text("SNAKE PRO - TSIS 4", WIDTH//2, 100, (0, 255, 0), True)
        draw_text(f"Enter Name: {username}_", WIDTH//2, 200, (255, 255, 0), True)
        draw_text("Press ENTER to Play", WIDTH//2, 300, center=True)
        draw_text("L - Leaderboard | S - Settings | Q - Quit", WIDTH//2, 400, (150, 150, 150), True)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username:
                    play_game(username, settings)
                elif event.key == pygame.K_BACKSPACE: 
                    username = username[:-1]
                elif event.key == pygame.K_l: 
                    leaderboard_screen()
                elif event.key == pygame.K_s: 
                    settings = settings_screen(settings)
                elif event.key == pygame.K_q: 
                    pygame.quit(); sys.exit()
                else:
                    if len(username) < 10 and event.unicode.isprintable():
                        username += event.unicode
        pygame.display.flip()
        clock.tick(60)

def play_game(username, settings):
    """Основной игровой цикл"""
    game = Game(settings)
    pb = get_personal_best(username) # Получаем личный рекорд из БД
    
    running = True
    while running:
        screen.fill((0, 0, 0))
        
        # Сетка (Пункт 3.5)
        if settings.get("grid_overlay", True):
            for x in range(0, WIDTH, CELL_SIZE):
                pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, CELL_SIZE):
                pygame.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and game.snake.direction != "DOWN": game.snake.direction = "UP"
                if event.key == pygame.K_DOWN and game.snake.direction != "UP": game.snake.direction = "DOWN"
                if event.key == pygame.K_LEFT and game.snake.direction != "RIGHT": game.snake.direction = "LEFT"
                if event.key == pygame.K_RIGHT and game.snake.direction != "LEFT": game.snake.direction = "RIGHT"

        # Движение
        head = game.snake.move()
        
        # Проверка столкновений (стены, препятствия, хвост)
        if game.check_collision(head):
            running = False
            
        # Еда (обычная)
        if head == game.food:
            game.score += 10
            game.food = [random.randrange(0, WIDTH//CELL_SIZE)*CELL_SIZE, random.randrange(0, HEIGHT//CELL_SIZE)*CELL_SIZE]
            # Увеличение уровня и скорости[cite: 2]
            if game.score % 30 == 0:
                game.level += 1
                game.speed += 2
                game.generate_obstacles() # Новые препятствия на уровне
        else:
            game.snake.body.pop()

        # Ядовитая еда (Пункт 3.2)
        if head == game.poison:
            if len(game.snake.body) <= 2: 
                running = False
            else:
                game.snake.body.pop()
                game.snake.body.pop()
            game.poison = [random.randrange(0, WIDTH//CELL_SIZE)*CELL_SIZE, random.randrange(0, HEIGHT//CELL_SIZE)*CELL_SIZE]

        # Отрисовка объектов
        pygame.draw.rect(screen, (255, 0, 0), (*game.food, CELL_SIZE, CELL_SIZE)) # Еда
        pygame.draw.rect(screen, (139, 0, 0), (*game.poison, CELL_SIZE, CELL_SIZE)) # Яд
        
        for block in game.obstacles: # Препятствия
            pygame.draw.rect(screen, (100, 100, 100), (*block, CELL_SIZE, CELL_SIZE))
            
        for segment in game.snake.body: # Змейка
            pygame.draw.rect(screen, game.snake.color, (*segment, CELL_SIZE, CELL_SIZE))

        # Статистика на экране
        draw_text(f"Score: {game.score} | Level: {game.level} | PB: {pb}", 10, 10)
        
        pygame.display.flip()
        clock.tick(game.speed)

    # Сохранение результата в PostgreSQL
    save_game_result(username, game.score, game.level)
    game_over_screen(username, game.score, game.level, pb)

def leaderboard_screen():
    """Экран топ-10 из базы"""
    scores = get_leaderboard()
    while True:
        screen.fill((20, 30, 20))
        draw_text("TOP 10 ALL-TIME", WIDTH//2, 50, (0, 255, 0), True)
        y = 120
        for i, (name, score, lvl, dt) in enumerate(scores):
            txt = f"{i+1}. {name} - {score} (Lvl {lvl})"
            draw_text(txt, 100, y)
            y += 35
        draw_text("Press B to go Back", WIDTH//2, 550, center=True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b: return
        pygame.display.flip()

def settings_screen(settings):
    """Экран настроек (JSON)"""
    while True:
        screen.fill((30, 30, 30))
        draw_text("SETTINGS", WIDTH//2, 100, center=True)
        draw_text(f"1. Grid: {'ON' if settings['grid_overlay'] else 'OFF'}", 200, 200)
        draw_text(f"2. Color: {settings['snake_color']}", 200, 250)
        draw_text("Press S to Save and Exit", WIDTH//2, 400, center=True)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: 
                    settings["grid_overlay"] = not settings["grid_overlay"]
                if event.key == pygame.K_s: 
                    save_settings(settings)
                    return settings
        pygame.display.flip()

def game_over_screen(name, score, level, pb):
    """Экран окончания игры"""
    while True:
        screen.fill((50, 0, 0))
        draw_text("GAME OVER", WIDTH//2, 150, (255, 255, 255), True)
        draw_text(f"Score: {score} | Level: {level}", WIDTH//2, 250, center=True)
        draw_text(f"Best: {max(score, pb)}", WIDTH//2, 300, (255, 255, 0), True)
        draw_text("Press SPACE for Menu", WIDTH//2, 400, center=True)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: return
        pygame.display.flip()

if __name__ == "__main__":
    menu_screen()