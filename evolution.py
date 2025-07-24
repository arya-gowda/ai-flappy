# flappy_ai/evolution.py
import torch
import random
import copy
from bird import Bird
from config import POPULATION_SIZE, MUTATION_RATE, SELECTION_RATE

def generate_initial_population():
    return [Bird() for _ in range(POPULATION_SIZE)]

def evaluate_fitness(population, pipes):
    for bird in population:
        bird.calculate_fitness(pipes)

def select_best(population):
    population.sort(key=lambda b: b.fitness, reverse=True)
    survivors = population[:int(POPULATION_SIZE * SELECTION_RATE)]
    return survivors

def crossover(parent1, parent2):
    child = copy.deepcopy(parent1)
    for child_param, p1_param, p2_param in zip(
        child.model.parameters(), parent1.model.parameters(), parent2.model.parameters()
    ):
        mask = torch.rand_like(p1_param) < 0.5
        child_param.data.copy_(torch.where(mask, p1_param.data, p2_param.data))
    return child

def mutate(bird):
    for param in bird.model.parameters():
        mutation_mask = torch.rand_like(param) < MUTATION_RATE
        noise = torch.randn_like(param) * 0.2
        param.data += mutation_mask * noise

def reproduce(survivors):
    new_generation = []
    while len(new_generation) < POPULATION_SIZE:
        parent1, parent2 = random.sample(survivors, 2)
        child = crossover(parent1, parent2)
        mutate(child)
        new_generation.append(child)
    return new_generation

def evolve_population(population):
    survivors = select_best(population)
    new_population = []
    while len(new_population) < len(population):
        p1, p2 = random.sample(survivors, 2)
        child = crossover(p1, p2)
        mutate(child)
        new_population.append(child)
    return new_population
