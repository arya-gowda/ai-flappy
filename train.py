from evolution import evolve_population, generate_initial_population
from inputs_fitness import get_nn_inputs, update_fitness
from pipe import Pipe
from bird import Bird
from logger import Logger
from config import SCREEN_WIDTH, SCREEN_HEIGHT, PIPE_SPACING, VISUALIZE, GENERATION_LIMIT, FPS
import pygame
import torch

pygame.init()

if VISUALIZE:
  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  clock = pygame.time.Clock()
  pygame.display.set_caption("AI Flappy Bird")

logger = Logger()

# -- Start training --
population = generate_initial_population()
quit = False

for generation in range(GENERATION_LIMIT):
  if quit:
    break

  pipes = [Pipe(SCREEN_WIDTH + i * PIPE_SPACING) for i in range(3)]
  for bird in population:
    bird.reset_state()
  ticks = 0

  while any(bird.alive for bird in population):
    if VISUALIZE:
      screen.fill("SkyBlue")
      pygame.display.set_caption(f"Generation: {generation} | Population Size: {len(population)}")

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        quit = True
        break
    
    if quit:
      break

    for pipe in pipes:
      pipe.update_pop(population)
      if pipe.off_screen():
        pipes.remove(pipe)
        pipes.append(Pipe(pipes[-1].x + PIPE_SPACING))
      if VISUALIZE:
        pipe.draw(screen)

    for bird in population:
      if bird.alive:
        inputs = get_nn_inputs(bird, pipes)
        bird.think(inputs)
        bird.update()
        update_fitness(bird)
        for pipe in pipes:
          if pipe.collides_with(bird):
            bird.alive = False
        if VISUALIZE:
          bird.draw(screen)

    if VISUALIZE:
      pygame.display.update()
      clock.tick(FPS)

    ticks += 1
  
  # -- End of generation processing --
  logger.log(generation, population)
  print(f"Generation {generation}: Max Fitness = {max(b.fitness for b in population)}")
  population = evolve_population(population)



# -- Save logs, plot, and best model --
logger.save()
logger.plot_avg()
logger.plot_max()

best_bird = max(population, key=lambda b: b.fitness)
torch.save(best_bird.model.state_dict(), "results/best_model.pth")

pygame.quit()