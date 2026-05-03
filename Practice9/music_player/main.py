import pygame
import sys
from player import MusicPlayer

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 700, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

font = pygame.font.Font(None, 36)

playlist = [
    ("/Users/dimash/Desktop/pp2-practice/Practice9/music_player/music/sample_tracks/track1.mp3", "Artist1 - Song 1"),
    ("/Users/dimash/Desktop/pp2-practice/Practice9/music_player/music/sample_tracks/track2.mp3", "Artist2 - Song 2")
]

player = MusicPlayer(playlist)
clock = pygame.time.Clock()

def draw_bar(x, y, width, height, progress):
    pygame.draw.rect(screen, (60, 60, 60), (x, y, width, height))
    pygame.draw.rect(screen, (0, 255, 100), (x, y, int(width * progress), height))

print("Программа запущена. Кликните на окно и нажмите P для старта.")

running = True
while running:
    screen.fill((25, 25, 25))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            print(f"Нажата клавиша: {pygame.key.name(event.key)}") 
            
            if event.key == pygame.K_p:
                if player.is_playing:
                    player.pause()
                else:
                    player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next()
            elif event.key == pygame.K_b:
                player.prev()

    title_text = player.get_title()
    title_surface = font.render(title_text, True, (255, 255, 255))
    screen.blit(title_surface, (20, 50))

    status_text = "PLAYING" if player.is_playing else ("PAUSED" if player.is_paused else "STOPPED")
    status_surface = font.render(status_text, True, (100, 100, 100))
    screen.blit(status_surface, (20, 90))

    pos = player.get_pos()
    progress = min(pos / 180, 1.0) 
    draw_bar(20, 150, 660, 10, progress)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()