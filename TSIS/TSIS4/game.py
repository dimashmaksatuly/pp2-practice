import pygame
import random

CELL_SIZE = 20
WIDTH, HEIGHT = 800, 600

class Snake:
    def __init__(self, color):
        self.body = [[100, 100], [80, 100], [60, 100]]
        self.direction = "RIGHT"
        self.color = color
        self.shield = False

    def move(self):
        head = list(self.body[0])
        if self.direction == "UP": head[1] -= CELL_SIZE
        elif self.direction == "DOWN": head[1] += CELL_SIZE
        elif self.direction == "LEFT": head[0] -= CELL_SIZE
        elif self.direction == "RIGHT": head[0] += CELL_SIZE
        self.body.insert(0, head)
        return head

class Game:
    def __init__(self, settings):
        self.settings = settings
        self.snake = Snake(settings["snake_color"])
        self.food = [random.randrange(1, WIDTH//CELL_SIZE)*CELL_SIZE, 
                     random.randrange(1, HEIGHT//CELL_SIZE)*CELL_SIZE]
        self.poison = [random.randrange(1, WIDTH//CELL_SIZE)*CELL_SIZE, 
                       random.randrange(1, HEIGHT//CELL_SIZE)*CELL_SIZE]
        self.powerup = None
        self.powerup_type = None
        self.powerup_timer = 0
        self.powerup_spawn_time = 0
        
        self.obstacles = []
        self.level = 1
        self.score = 0
        self.speed = 10

    def generate_obstacles(self):
        """Препятствия с 3-го уровня (Пункт 3.4)"""
        self.obstacles = []
        if self.level >= 3:
            for _ in range(self.level * 2):
                obs = [random.randrange(1, WIDTH//CELL_SIZE)*CELL_SIZE, 
                       random.randrange(1, HEIGHT//CELL_SIZE)*CELL_SIZE]
                # Проверка, чтобы не заспавнить на змейке
                if obs not in self.snake.body:
                    self.obstacles.append(obs)

    def check_collision(self, head):
        # Границы и препятствия
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT or head in self.obstacles:
            if self.snake.shield:
                self.snake.shield = False
                return False
            return True
        # Самоедство
        if head in self.snake.body[1:]:
            if self.snake.shield:
                self.snake.shield = False
                return False
            return True
        return False