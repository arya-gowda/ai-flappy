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
        self.rect = self.image.get_rect(center=(200,200))
        self.gravity = 0

    def bird_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE] or pressed[pygame.K_UP]:
            self.gravity = -30

    def apply_gravity(self):
        self.gravity += 2
        self.rect.y += self.gravity
        if self.rect.bottom >= 700:
            self.rect.bottom = 700

    def update(self):
        self.bird_input()
        self.apply_gravity()

class PipeUpper(pygame.sprite.Sprite):
    def __init__(self, y_pos) -> None:
        super().__init__()

        self.image = pygame.Surface((60, 600))
        self.image.fill("Green")
        self.rect = self.image.get_rect(bottomleft=(1800,y_pos-60))

    def destroy(self):
        if self.rect.right < 0:
            self.kill()

    def update(self):
        self.rect.x -= 10

class PipeLower(pygame.sprite.Sprite):
    def __init__(self, y_pos) -> None:
        super().__init__()

        self.image = pygame.Surface((60, 600))
        self.image.fill("Green")
        self.rect = self.image.get_rect(topleft=(1800,y_pos+60))
        # pygame.draw.rect(self.image,"Green",self.rect)

    def destroy(self):
        if self.rect.right < 0:
            self.kill()

    def update(self):
        self.rect.x -= 10
        self.destroy()


def collision_sprite():
    if pygame.sprite.spritecollide(bird.sprite,obstacle_group,False):
        obstacle_group.empty()
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

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,4000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == obstacle_timer:
            print("trigger")
            random_y = randint(100,600)
            obstacle_group.add(PipeUpper(y_pos=random_y))
            obstacle_group.add(PipeLower(y_pos=random_y))
            print(1)

    # set background white
    screen.fill('White')
    # bird_rect = pygame.draw.circle(screen, 'Yellow', (200,bird_y_pos), 30)

    bird.draw(screen)
    bird.update()

    obstacle_group.draw(screen)
    obstacle_group.update()
    
    pygame.draw.rect(screen, 'Black', pygame.Rect(0,700,1600,100))


    # update everything
    pygame.display.update()
    clock.tick(60)