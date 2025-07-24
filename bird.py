import pygame
import torch
import torch.nn as nn
import config

BIRD_START_X = 250
BIRD_START_Y = 250
GRAVITY = 1
GROUND_Y = 800
FLAP_STRENGTH = 15

class Bird:
    def __init__(self):
        self.x = BIRD_START_X
        self.y = BIRD_START_Y
        self.velocity = 0
        self.alive = True
        self.fitness = 0
        self.just_passed_pipe = False

        self.model = NeuralNet()

    def reset_state(self):
        self.x = BIRD_START_X
        self.y = BIRD_START_Y
        self.velocity = 0
        self.alive = True
        self.fitness = 0
        self.just_passed_pipe = False

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        if self.y >= GROUND_Y or self.y <= 0:
            self.alive = False

    def think(self, inputs):
        tensor_inputs = torch.tensor(inputs, dtype=torch.float32)
        output = self.model(tensor_inputs)
        if output.item() > 0.5:
            self.flap()

    def flap(self):
        self.velocity = -FLAP_STRENGTH

    def draw(self, screen):
        pygame.draw.circle(screen, "Yellow", (int(self.x), int(self.y)), config.BIRD_RADIUS)

    def clone(self):
        new_bird = Bird()
        new_bird.model.load_state_dict(self.model.state_dict())
        return new_bird
    
    def calculate_fitness(self, score, survived_time):
        self.fitness = score * 10 + survived_time
    
class NeuralNet(nn.Module):
    def __init__(self):
        super(NeuralNet, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(4, 8),
            nn.ReLU(),
            nn.Linear(8, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.model(x)
