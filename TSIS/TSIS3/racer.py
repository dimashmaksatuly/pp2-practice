import pygame
import random

WIDTH = 400
HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self, color_name="red"):
        super().__init__()
        self.image = pygame.Surface((40, 70))
        # Настройка цвета из Settings (Пункт 3.5)
        colors = {"red": (255, 0, 0), "blue": (0, 0, 255), "green": (0, 255, 0)}
        self.image.fill(colors.get(color_name, (255, 0, 0)))
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        
        self.speed = 5
        self.lives = 1
        
        # Переменные для Power-ups (Пункт 3.3)
        self.active_powerup = None
        self.powerup_timer = 0
        self.shielded = False
        self.nitro = False

    def activate_powerup(self, p_type):
        self.active_powerup = p_type
        self.powerup_timer = pygame.time.get_ticks()
        if p_type == "shield":
            self.shielded = True
        elif p_type == "nitro":
            self.nitro = True
        elif p_type == "repair":
            self.lives += 1
            self.active_powerup = None  # Срабатывает мгновенно

    def update(self):
        keys = pygame.key.get_pressed()
        move_speed = self.speed * (2 if self.nitro else 1)
        
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= move_speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += move_speed
            
        # Таймер усилителей (исчезают через 4 секунды)
        if self.active_powerup:
            if pygame.time.get_ticks() - self.powerup_timer > 4000:
                self.nitro = False
                if self.active_powerup != "shield":  # Щит держится до удара
                    self.active_powerup = None

class Traffic(pygame.sprite.Sprite):
    def __init__(self, speed_modifier):
        super().__init__()
        self.image = pygame.Surface((40, 70))
        self.image.fill((150, 0, 0)) # Встречные машины темно-красные
        self.rect = self.image.get_rect()
        self.speed_modifier = speed_modifier
        self.reset()

    def reset(self):
        lanes = [WIDTH//6, WIDTH//2, 5*WIDTH//6]
        self.rect.center = (random.choice(lanes), random.randint(-400, -100))
        self.speed = random.randint(3, 6) + self.speed_modifier

    def update(self, nitro_active):
        self.rect.y += self.speed + (5 if nitro_active else 0)
        if self.rect.top > HEIGHT:
            self.reset()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 20)) # Барьер
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        lanes = [WIDTH//6, WIDTH//2, 5*WIDTH//6]
        self.rect.center = (random.choice(lanes), random.randint(-600, -200))
        self.speed = 3

    def update(self, nitro_active):
        self.rect.y += self.speed + (5 if nitro_active else 0)
        if self.rect.top > HEIGHT:
            self.reset()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 215, 0), (10, 10), 10)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(40, WIDTH-40), random.randint(-300, -50))
        self.speed = 3

    def update(self, nitro_active):
        self.rect.y += self.speed + (5 if nitro_active else 0)
        if self.rect.top > HEIGHT:
            self.reset()

class PowerUpItem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(["nitro", "shield", "repair"])
        self.image = pygame.Surface((25, 25))
        # Цвета: Нитро - голубой, Щит - желтый, Ремонт - зеленый
        if self.type == "nitro": self.image.fill((0, 255, 255))
        elif self.type == "shield": self.image.fill((255, 255, 0))
        elif self.type == "repair": self.image.fill((0, 255, 0))
        
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.type = random.choice(["nitro", "shield", "repair"])
        if self.type == "nitro": self.image.fill((0, 255, 255))
        elif self.type == "shield": self.image.fill((255, 255, 0))
        elif self.type == "repair": self.image.fill((0, 255, 0))
        
        self.rect.center = (random.randint(40, WIDTH-40), random.randint(-1000, -500))
        self.speed = 3

    def update(self, nitro_active):
        self.rect.y += self.speed + (5 if nitro_active else 0)
        if self.rect.top > HEIGHT:
            self.reset()