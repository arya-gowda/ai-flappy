import pygame
import random
import config

class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = config.PIPE_WIDTH
        self.gap = config.PIPE_GAP
        self.top = random.randint(100, config.SCREEN_HEIGHT - self.gap - 100)
        self.bottom = self.top + self.gap

    def update(self):
        self.x -= config.PIPE_SPEED

    def update_pop(self, population):
        self.x -= config.PIPE_SPEED

        for bird in population:
            if self.x + self.width < bird.x and bird.x < self.x + self.width + config.PIPE_SPEED:
                bird.just_passed_pipe = True
                print("pipe passed")

    def draw(self, screen):
        # Top pipe
        pygame.draw.rect(screen, "Green", pygame.Rect(self.x, 0, self.width, self.top))
        # Bottom pipe
        pygame.draw.rect(screen, "Green", pygame.Rect(self.x, self.bottom, self.width, config.SCREEN_HEIGHT - self.bottom))

    def off_screen(self):
        return self.x + self.width < 0

    def collides_with(self, bird):
        bird_rect = pygame.Rect(bird.x - config.BIRD_RADIUS, bird.y - config.BIRD_RADIUS, config.BIRD_RADIUS*2, config.BIRD_RADIUS*2)
        top_rect = pygame.Rect(self.x, 0, self.width, self.top)
        bottom_rect = pygame.Rect(self.x, self.bottom, self.width, config.SCREEN_HEIGHT - self.bottom)
        return bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect)
