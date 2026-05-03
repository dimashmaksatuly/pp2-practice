import pygame

def flood_fill(surf, x, y, new_color, width, height):
    """Алгоритм заливки на основе стека"""
    target_color = surf.get_at((x, y))
    if target_color == new_color:
        return
    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        if surf.get_at((cx, cy)) == target_color:
            surf.set_at((cx, cy), new_color)
            # Проверка соседних пикселей (вверх, вниз, влево, вправо)
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < width and 0 <= ny < height:
                    stack.append((nx, ny))

def draw_rhombus(surf, color, start_pos, curr_pos, thickness):
    """Отрисовка ромба по двум точкам"""
    points = [
        (start_pos[0], start_pos[1] + (curr_pos[1] - start_pos[1]) // 2),
        (start_pos[0] + (curr_pos[0] - start_pos[0]) // 2, start_pos[1]),
        (curr_pos[0], start_pos[1] + (curr_pos[1] - start_pos[1]) // 2),
        (start_pos[0] + (curr_pos[0] - start_pos[0]) // 2, curr_pos[1])
    ]
    pygame.draw.polygon(surf, color, points, thickness)