import pygame
import sys
from ui import Button, draw_text, input_name_screen
from persistence import load_settings, save_settings, load_leaderboard, save_score
from racer import Player, Traffic, Obstacle, PowerUpItem, Coin, WIDTH, HEIGHT

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 3: Racer Pro")
clock = pygame.time.Clock()

def play_game(player_name, settings):
    # Сложность
    diff_multiplier = {"Easy": 0, "Medium": 2, "Hard": 4}.get(settings["difficulty"], 2)
    
    player = Player(settings["car_color"])
    
    enemies = pygame.sprite.Group()
    for _ in range(3): enemies.add(Traffic(diff_multiplier))
        
    obstacles = pygame.sprite.Group()
    obstacles.add(Obstacle())
    
    coins = pygame.sprite.Group()
    for _ in range(3): coins.add(Coin())
        
    powerups = pygame.sprite.Group()
    powerups.add(PowerUpItem())
    
    all_sprites = pygame.sprite.Group(player, enemies, obstacles, coins, powerups)
    
    score = 0
    distance = 0.0
    running = True
    
    while running:
        clock.tick(60)
        nitro_active = player.nitro
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
                
        # Обновление всех спрайтов
        for s in all_sprites:
            if s == player:
                s.update()
            else:
                s.update(nitro_active)
            
        # Сбор монет
        hits = pygame.sprite.spritecollide(player, coins, False)
        for hit in hits:
            score += 10
            hit.reset()
            
        # Сбор усилителей (Пункт 3.3)
        hits = pygame.sprite.spritecollide(player, powerups, False)
        for hit in hits:
            player.activate_powerup(hit.type)
            hit.reset()
            
        # Столкновения с врагами и препятствиями (Пункт 3.2)
        hits_enemy = pygame.sprite.spritecollide(player, enemies, False)
        hits_obs = pygame.sprite.spritecollide(player, obstacles, False)
        
        if hits_enemy or hits_obs:
            if player.shielded:
                player.shielded = False
                player.active_powerup = None
                if hits_enemy: hits_enemy[0].reset()
                if hits_obs: hits_obs[0].reset()
            else:
                player.lives -= 1
                if hits_enemy: hits_enemy[0].reset()
                if hits_obs: hits_obs[0].reset()
                
            if player.lives <= 0:
                running = False
        
        # Дистанция и сложность (Пункт 3.4 и 3.2)
        distance += (0.1 if not nitro_active else 0.3)
        diff_modifier = int(distance / 100)
        for e in enemies:
            e.speed_modifier = diff_multiplier + diff_modifier
        
        # Отрисовка
        screen.fill((50, 50, 50)) # Дорога
        for i in range(1, 3): # Разметка полос
            pygame.draw.line(screen, (255, 255, 255), (i * WIDTH//3, 0), (i * WIDTH//3, HEIGHT), 5)
            
        all_sprites.draw(screen)
        
        # Отрисовка UI в игре
        draw_text(screen, f"Score: {score}", 20, 10, 10)
        draw_text(screen, f"Dist: {int(distance)}m", 20, 10, 35)
        draw_text(screen, f"Lives: {player.lives}", 20, 10, 60)
        
        if player.active_powerup:
            time_left = max(0, 4 - (pygame.time.get_ticks() - player.powerup_timer)//1000)
            if player.active_powerup == "shield":
                draw_text(screen, "SHIELD ACTIVE", 20, 10, 85, (255, 255, 0))
                pygame.draw.circle(screen, (255, 255, 0), player.rect.center, 40, 2)
            else:
                draw_text(screen, f"NITRO ({time_left}s)", 20, 10, 85, (0, 255, 255))
        
        pygame.display.flip()
        
    save_score(player_name, score, distance)
    game_over_screen(score, distance)

def game_over_screen(score, distance):
    btn_menu = Button(100, 400, 200, 50, "MAIN MENU", (100, 100, 100))
    while True:
        screen.fill((50, 20, 20))
        draw_text(screen, "GAME OVER", 40, 200, 150, center=True)
        draw_text(screen, f"Score: {score}", 25, 200, 220, center=True)
        draw_text(screen, f"Distance: {int(distance)}m", 25, 200, 260, center=True)
        
        btn_menu.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if btn_menu.is_clicked(event):
                return
        pygame.display.flip()
        clock.tick(60)

def show_settings(settings):
    colors = ["red", "blue", "green"]
    diffs = ["Easy", "Medium", "Hard"]
    
    btn_color = Button(100, 200, 200, 50, f"Color: {settings['car_color']}")
    btn_diff = Button(100, 280, 200, 50, f"Diff: {settings['difficulty']}")
    btn_back = Button(100, 400, 200, 50, "BACK", (100, 100, 100))
    
    while True:
        screen.fill((30, 30, 30))
        draw_text(screen, "SETTINGS", 40, 200, 100, center=True)
        
        btn_color.text = f"Color: {settings['car_color']}"
        btn_diff.text = f"Diff: {settings['difficulty']}"
        
        btn_color.draw(screen)
        btn_diff.draw(screen)
        btn_back.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if btn_color.is_clicked(event):
                idx = (colors.index(settings['car_color']) + 1) % len(colors)
                settings['car_color'] = colors[idx]
            if btn_diff.is_clicked(event):
                idx = (diffs.index(settings['difficulty']) + 1) % len(diffs)
                settings['difficulty'] = diffs[idx]
            if btn_back.is_clicked(event):
                save_settings(settings)
                return settings
        pygame.display.flip()
        clock.tick(60)

def show_leaderboard():
    board = load_leaderboard()
    btn_back = Button(100, 500, 200, 50, "BACK", (100, 100, 100))
    while True:
        screen.fill((20, 20, 50))
        draw_text(screen, "TOP 10 SCORES", 35, 200, 50, center=True)
        
        y = 120
        for i, entry in enumerate(board):
            text = f"{i+1}. {entry['name']} - {entry['score']} pts - {entry['distance']}m"
            draw_text(screen, text, 18, 50, y)
            y += 35
            
        btn_back.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if btn_back.is_clicked(event):
                return
        pygame.display.flip()
        clock.tick(60)

def main():
    settings = load_settings()
    
    btn_play = Button(100, 200, 200, 50, "PLAY", (0, 150, 0))
    btn_lb = Button(100, 280, 200, 50, "LEADERBOARD", (150, 100, 0))
    btn_set = Button(100, 360, 200, 50, "SETTINGS", (0, 100, 150))
    btn_quit = Button(100, 440, 200, 50, "QUIT", (150, 0, 0))
    
    while True:
        screen.fill((20, 20, 20))
        draw_text(screen, "RACER PRO", 45, 200, 100, (255, 255, 0), center=True)
        
        btn_play.draw(screen)
        btn_lb.draw(screen)
        btn_set.draw(screen)
        btn_quit.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if btn_play.is_clicked(event):
                name = input_name_screen(screen)
                if name:
                    play_game(name, settings)
            if btn_lb.is_clicked(event):
                show_leaderboard()
            if btn_set.is_clicked(event):
                settings = show_settings(settings)
            if btn_quit.is_clicked(event):
                pygame.quit(); sys.exit()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()