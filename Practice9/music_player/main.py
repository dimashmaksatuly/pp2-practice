import pygame
from player import MusicPlayer

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((600, 200))
pygame.display.set_caption("Music Player")

font = pygame.font.Font(None, 36)

playlist = [
    "music_player/music/sample_tracks/track1.mp3",
    "music_player/music/sample_tracks/track2.mp3"
]

player = MusicPlayer(playlist)

def draw():
    screen.fill((30, 30, 30))
    text = font.render(f"Track: {player.get_current_track()}", True, (255, 255, 255))
    screen.blit(text, (20, 80))
    pygame.display.flip()

running = True
while running:
    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next()
            elif event.key == pygame.K_b:
                player.previous()
            elif event.key == pygame.K_q:
                running = False

pygame.quit()