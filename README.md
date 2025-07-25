# 🧠 Flappy Bird Neuroevolution

[![Python Version](https://img.shields.io/badge/python-3.13.1-blue.svg)](https://www.python.org/downloads/release/python-3131/)
[![Last Commit](https://img.shields.io/github/last-commit/arya-gowda/ai-flappy)](https://github.com/arya-gowda/ai-flappy)
[![License](https://img.shields.io/github/license/arya-gowda/ai-flappy)](LICENSE)

A neural network–controlled Flappy Bird agent trained using a genetic algorithm (GA). The bird learns to play by evolving its neural network through generations of gameplay.

(media/flappy_demo.gif)

---

## 📁 Project Structure

| File | Purpose |
|------|---------|
| `train.py` | Main training loop for evolving bird agents. |
| `main_game.py` | Runs the best-performing trained bird model. |
| `bird.py` | Defines the Bird agent and its neural network. |
| `pipe.py` | Contains the Pipe object and collision logic. |
| `evolution.py` | Handles genetic algorithm: selection, crossover, mutation. |
| `inputs_fitness.py` | Extracts neural net inputs and computes fitness. |
| `config.py` | Global configuration (screen size, NN size, constants, etc). |
| `logger.py` | Logging and output tracking for training progress. |

---

## 🧠 Neural Network

Each bird is controlled by a simple feedforward neural network.

### Inputs to the Neural Network:
1. **Bird Y-position** (`bird_y`)  
2. **Bird Vertical Velocity** (`bird_velocity`)  
3. **Horizontal Distance to Next Pipe** (`pipe_dx`)  
4. **Vertical Distance to Pipe Gap Center** (`pipe_dy`)

### Output:
- A single float value.
- If `output > threshold` (e.g. 0.5), the bird flaps.

---

## 🧬 Genetic Algorithm Overview

The genetic algorithm evolves bird neural networks over generations.

### Steps:
- **Initialization**: Random neural networks
- **Fitness Evaluation**: Based on distance traveled and pipes passed
- **Selection**: Top performers become parents
- **Crossover**: Combine weights of parents
- **Mutation**: Add small random noise to offspring

---

## 🚀 How to Run

### Train the Agent
```bash
python train.py
```

### Train the Agent
```bash
python train.py
```

---

## ⚙️ Configurable Settings (`config.py`)
- `GENERATION_LIMIT`: Number of generations run
- `POPULATION_SIZE`
- `MUTATION_RATE`: GA mutation rate
- `SELECTION_RATE`: GA selection rate
- `SCREEN_WIDTH`
- `SCREEN_HEIGHT`
- `PIPE_GAP`: Pipe gap size
- `PIPE_WIDTH`
- `PIPE_SPEED`
- `PIPE_SPACING`: Distance between pipes
- `BIRD_RADIUS`: Bird size
- `FPS`
- `VISUALIZE`: Training visualization option

---

## 📊 Logging

`logger.py` logs:

- Training log with max fitnesses by generation  
- Best and average fitness plots
- Best performing model saved  

---

## 📝 Potential Improvements

- Use recurrent neural networks (RNNs)  
- Improve the fitness function for better learning curves
- Save and load training checkpoints
