import math

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800
PIPE_GAP = 150

# Assume these come from the actual game state
def get_next_pipe(bird_x, pipes):
    # Returns the next pipe ahead of the bird
    """
    Returns the next pipe ahead of the bird
    Input: Bird x position and list of Pipe objects
    Output: Pipe object of next pipe
    """
    for pipe in pipes:
        if pipe.x + pipe.width > bird_x:
            return pipe
    return None

def get_nn_inputs(bird, pipes):
    """
    Returns normalized input features for the neural network
    Input: Bird object and list of Pipe objects
    Output: [bird_y, bird_velocity, horizontal_dist, vertical_dist]
    """
    next_pipe = get_next_pipe(bird.x, pipes)
    
    if next_pipe is None:
        return [0.5, 0.0, 1.0, 0.0]  # Default if no pipe

    # Vertical center of the pipe gap
    gap_y = next_pipe.top

    # Normalize values to [0, 1] range
    norm_bird_y = bird.y / SCREEN_HEIGHT
    norm_velocity = bird.velocity / 20.0  # assume max speed ~20
    norm_horizontal_dist = (next_pipe.x - bird.x) / SCREEN_WIDTH
    norm_vertical_dist = (gap_y - bird.y) / SCREEN_HEIGHT

    return [norm_bird_y, norm_velocity, norm_horizontal_dist, norm_vertical_dist]

def update_fitness(bird):
    """Update fitness score based on bird's survival"""
    """
    Update fitness score based on bird's survival
    Input: Bird object
    Output: NONE
    """
    bird.fitness += 1

    if bird.just_passed_pipe:
        bird.fitness += 50
        bird.just_passed_pipe = False
