import pygame
import os

class MusicPlayer:
    def __init__(self, playlist):
        self.playlist = playlist
        self.current = 0
        self.is_playing = False
        self.is_paused = False

    def load(self):
        file_path = self.playlist[self.current][0]
        if os.path.exists(file_path):
            try:
                pygame.mixer.music.load(file_path)
                return True
            except Exception as e:
                print(f"Ошибка загрузки файла: {e}")
                return False
        else:
            print(f"Файл не найден: {file_path}")
            return False

    def play(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.is_playing = True
            print("Продолжаем воспроизведение...")
        else:
            if self.load():
                pygame.mixer.music.play()
                self.is_playing = True
                print(f"Играет: {self.get_title()}")

    def pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.is_paused = True
            print("Пауза")

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        print("Стоп")

    def next(self):
        self.current = (self.current + 1) % len(self.playlist)
        self.is_paused = False
        self.play()

    def prev(self):
        self.current = (self.current - 1) % len(self.playlist)
        self.is_paused = False
        self.play()

    def get_title(self):
        return self.playlist[self.current][1]

    def get_pos(self):
        if self.is_playing or self.is_paused:
            return max(0, pygame.mixer.music.get_pos() / 1000)
        return 0