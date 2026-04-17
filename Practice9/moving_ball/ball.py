class Ball:
    def __init__(self, x, y, radius, speed, width, height):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.width = width
        self.height = height

    def move(self, direction):
        if direction == "up" and self.y - self.speed - self.radius >= 0:
            self.y -= self.speed
        elif direction == "down" and self.y + self.speed + self.radius <= self.height:
            self.y += self.speed
        elif direction == "left" and self.x - self.speed - self.radius >= 0:
            self.x -= self.speed
        elif direction == "right" and self.x + self.speed + self.radius <= self.width:
            self.x += self.speed