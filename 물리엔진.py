import pygame
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Physics Engine")
clock = pygame.time.Clock()

WHITE, RED, BLACK = (255, 255, 255), (255, 0, 0), (0, 0, 0)

gravity = 0.5

class Ball:
    def __init__(self, x, y, radius):
        self.x, self.y, self.radius = x, y, radius
        self.velocity = [0, 0]
    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)
    def update(self, gravity):
        self.velocity[1] += gravity
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        if self.y + self.radius > 600: 
            self.y, self.velocity[1] = 600 - self.radius, -self.velocity[1] * 0.8
        if self.x + self.radius > 800 or self.x - self.radius < 0: 
            self.velocity[0] = -self.velocity[0] * 0.8

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)
        screen.blit(pygame.font.Font(None, 36).render(self.text, True, BLACK), (self.rect.x + 10, self.rect.y + 10))
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Arrow:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.direction = direction
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)
        if self.direction == "up": pygame.draw.polygon(screen, BLACK, [(self.rect.centerx, self.rect.y), (self.rect.x + 10, self.rect.y + 20), (self.rect.x + 20, self.rect.y + 20)])
        elif self.direction == "down": pygame.draw.polygon(screen, BLACK, [(self.rect.centerx, self.rect.bottom), (self.rect.x + 10, self.rect.bottom - 20), (self.rect.x + 20, self.rect.bottom - 20)])
        elif self.direction == "left": pygame.draw.polygon(screen, BLACK, [(self.rect.x, self.rect.centery), (self.rect.x + 20, self.rect.y + 10), (self.rect.x + 20, self.rect.y + 20)])
        elif self.direction == "right": pygame.draw.polygon(screen, BLACK, [(self.rect.right, self.rect.centery), (self.rect.right - 20, self.rect.y + 10), (self.rect.right - 20, self.rect.y + 20)])
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

ball = Ball(400, 100, 20)
buttons = {
    "start": Button(50, 500, 100, 50, "Start"),
    "reset": Button(200, 500, 100, 50, "Reset")
}
arrows = {
    "gravity_up": Arrow(650, 100, "up"),
    "gravity_down": Arrow(650, 150, "down"),
    "force_up": Arrow(650, 250, "up"),
    "force_down": Arrow(650, 300, "down"),
    "angle_up": Arrow(650, 400, "up"),
    "angle_down": Arrow(650, 450, "down"),
    "pos_up": Arrow(50, 100, "up"),
    "pos_down": Arrow(50, 150, "down"),
    "pos_left": Arrow(20, 125, "left"),
    "pos_right": Arrow(80, 125, "right")
}

force, angle, running = 0.0, 0.0, False

running_game = True
while running_game:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_game = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if buttons["start"].is_clicked(event.pos):
                running = True
                ball.velocity = [force * math.cos(math.radians(angle)), 
                                 -force * math.sin(math.radians(angle))]
            if buttons["reset"].is_clicked(event.pos):
                ball.x, ball.y, ball.velocity, running = 400, 100, [0, 0], False
            if arrows["gravity_up"].is_clicked(event.pos): 
                gravity += 0.1
            if arrows["gravity_down"].is_clicked(event.pos): 
                gravity -= 0.1
            if arrows["force_up"].is_clicked(event.pos): force += 1
            if arrows["force_down"].is_clicked(event.pos): force -= 1
            if arrows["angle_up"].is_clicked(event.pos): angle += 5
            if arrows["angle_down"].is_clicked(event.pos): angle -= 5
            if arrows["pos_up"].is_clicked(event.pos) and not running: ball.y -= 5
            if arrows["pos_down"].is_clicked(event.pos) and not running: ball.y += 5
            if arrows["pos_left"].is_clicked(event.pos) and not running: ball.x -= 5
            if arrows["pos_right"].is_clicked(event.pos) and not running: ball.x += 5

    for button in buttons.values():
        button.draw(screen)
    for arrow in arrows.values():
        arrow.draw(screen)

    font = pygame.font.Font(None, 36)
    screen.blit(font.render(f"Gravity: {gravity:.1f}", True, BLACK), (500, 125))
    screen.blit(font.render(f"+Force: {force:.1f}", True, BLACK), (500, 275))
    screen.blit(font.render(f"Angle: {angle:.1f}", True, BLACK), (500, 425))

    if running:
        ball.update(gravity)
    ball.draw(screen)
    pygame.draw.line(screen, BLACK, (ball.x, ball.y), (ball.x + 50 * math.cos(math.radians(angle)), ball.y - 50 * math.sin(math.radians(angle))), 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
