import pygame
import os

class MusicPlayer:
    def __init__(self, playlist):
        self.playlist = playlist
        self.current = 0
        self.is_playing = False

    def load(self):
        pygame.mixer.music.load(self.playlist[self.current][0])

    def play(self):
        self.load()
        pygame.mixer.music.play()
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next(self):
        self.current = (self.current + 1) % len(self.playlist)
        self.play()

    def prev(self):
        self.current = (self.current - 1) % len(self.playlist)
        self.play()

    def get_title(self):
        return self.playlist[self.current][1]

    def get_pos(self):
        return pygame.mixer.music.get_pos() / 1000  # seconds