import pygame
import torch
from bird import Bird
from pipe import Pipe
from inputs_fitness import get_nn_inputs
import config
from logger import Logger

pygame.init()
logger = Logger()
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
clock = pygame.time.Clock()

def main():
    bird = Bird()
    bird.model.load_state_dict(torch.load("results/best_model.pth"))
    bird.model.eval()

    pipes = [Pipe(config.SCREEN_WIDTH + i * config.PIPE_SPACING) for i in range(3)]

    running = True
    while running:
        screen.fill("SkyBlue")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for pipe in pipes:
            pipe.update()
            if pipe.off_screen():
                pipes.remove(pipe)
                pipes.append(Pipe(pipes[-1].x + config.PIPE_SPACING))
            pipe.draw(screen)

        if bird.alive:
            inputs = get_nn_inputs(bird, pipes)
            bird.think(inputs)
            bird.update()
            bird.draw(screen)

        pygame.display.update()
        clock.tick(config.FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
