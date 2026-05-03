import pygame

class Button:
    def __init__(self, x, y, w, h, text, color=(70, 70, 70), hover_color=(100, 100, 100)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont("Verdana", 24, bold=True)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        
        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=10)
        
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

def draw_text(screen, text, size, x, y, color=(255, 255, 255), center=False):
    font = pygame.font.SysFont("Verdana", size, bold=True)
    surf = font.render(str(text), True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surf, rect)

def input_name_screen(screen):
    """Экран ввода имени (Пункт 3.4)"""
    clock = pygame.time.Clock()
    name = ""
    running = True
    
    while running:
        screen.fill((30, 30, 50))
        draw_text(screen, "ENTER YOUR NAME:", 30, 200, 200, center=True)
        
        # Поле ввода
        pygame.draw.rect(screen, (0, 0, 0), (50, 250, 300, 50), border_radius=5)
        pygame.draw.rect(screen, (255, 255, 255), (50, 250, 300, 50), 2, border_radius=5)
        draw_text(screen, name + "_", 30, 60, 255, (255, 255, 0))
        
        draw_text(screen, "Press ENTER to start", 20, 200, 350, (150, 150, 150), center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(name) > 0:
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 12 and event.unicode.isprintable():
                    name += event.unicode
                    
        pygame.display.flip()
        clock.tick(60)