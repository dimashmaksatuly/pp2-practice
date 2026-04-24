import pygame
from player import MusicPlayer

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 700, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

font = pygame.font.Font(None, 36)

playlist = [
    ("/Users/dimash/Desktop/pp2-practice/Practice9/music_player/music/sample_tracks/track1", "Artist1 - Song 1"),
    ("/Users/dimash/Desktop/pp2-practice/Practice9/music_player/music/sample_tracks/track2", "Artist2 - Song 2")
]

player = MusicPlayer(playlist)

clock = pygame.time.Clock()

def draw_bar(x, y, width, height, progress):
    pygame.draw.rect(screen, (80, 80, 80), (x, y, width, height))
    pygame.draw.rect(screen, (0, 200, 0), (x, y, width * progress, height))

running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            if event.key == pygame.K_s:
                player.stop()
            if event.key == pygame.K_n:
                player.next()
            if event.key == pygame.K_b:
                player.prev()

    title = font.render(player.get_title(), True, (255, 255, 255))
    screen.blit(title, (20, 50))

    # трекбар
    pos = player.get_pos()
    progress = min(pos / 10, 1)  # условная длина (10 сек)

    draw_bar(20, 150, 600, 20, progress)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()