from typing import Any
import pygame
from sys import exit
from random import randint

import pygame.locals


class Bird(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(self.image, "Yellow", (25, 25), 25)
        self.rect = self.image.get_rect(center=(250,250))
        self.gravity = 0

    def bird_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE] or pressed[pygame.K_UP]:
            self.gravity = -15

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 700:
            self.rect.bottom = 700
            pygame.event.post(pygame.event.Event(pygame.USEREVENT + 2))

    def update(self):
        self.bird_input()
        self.apply_gravity()

class PipeUpper(pygame.sprite.Sprite):
    def __init__(self, y_pos) -> None:
        super().__init__()

        self.image = pygame.Surface((60, 600))
        self.image.fill("Green")
        self.rect = self.image.get_rect(bottomleft=(1600,y_pos-75))
        self.passed = False

    def destroy(self):
        if self.rect.right < 0:
            self.kill()

    def update(self):
        self.rect.x -= 10
        self.destroy()

class PipeLower(pygame.sprite.Sprite):
    def __init__(self, y_pos) -> None:
        super().__init__()

        self.image = pygame.Surface((60, 600))
        self.image.fill("Green")
        self.rect = self.image.get_rect(topleft=(1600,y_pos+75))

    def destroy(self):
        if self.rect.right < 0:
            self.kill()

    def update(self):
        self.rect.x -= 10
        self.destroy()


def collision_sprite():
    if pygame.sprite.spritecollide(bird.sprite,obstacle_group,False):
        return False
    return True

pygame.init()

screen = pygame.display.set_mode((1600, 800))
clock = pygame.time.Clock()

white = (255,255,255)

game_active = True
score = 0

bird = pygame.sprite.GroupSingle()
bird.add(Bird())
obstacle_group = pygame.sprite.Group()
bg_rect = pygame.Rect(0,0,1600,600)

GROUND_COLLISION_EVENT = pygame.USEREVENT + 2

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,4000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == obstacle_timer and game_active:
            random_y = randint(300, 550)
            obstacle_group.add(PipeUpper(y_pos=random_y))
            obstacle_group.add(PipeLower(y_pos=random_y))
        if event.type == GROUND_COLLISION_EVENT:
            game_active = False

    screen.fill('White')
    bird.draw(screen)
    obstacle_group.draw(screen)
    pygame.draw.rect(screen, 'Black', pygame.Rect(0, 700, 1600, 100))
    font = pygame.font.Font(None, 50)
    score_surface = font.render(f'Score: {score}', True, 'Black')
    screen.blit(score_surface, (50, 50))

    if game_active:
        bird.update()
        obstacle_group.update()

        for obstacle in obstacle_group:
            if isinstance(obstacle, PipeUpper) and not obstacle.passed:
                if obstacle.rect.right < bird.sprite.rect.left:
                    obstacle.passed = True
                    score += 1

        game_active = collision_sprite()

    else:
        # Optional: Draw Game Over screen/text
        font = pygame.font.Font(None, 100)
        text = font.render("Game Over", True, "Red")
        text_rect = text.get_rect(center=(800, 300))
        screen.blit(text, text_rect)

        subfont = pygame.font.Font(None, 50)
        subtext = subfont.render("Press SPACE to Restart", True, "Black")
        subtext_rect = subtext.get_rect(center=(800, 400))
        screen.blit(subtext, subtext_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            bird.sprite.rect.center = (200, 200)
            bird.sprite.gravity = 0
            obstacle_group.empty()
            score = 0
            game_active = True

    pygame.display.update()
    clock.tick(60)
