import pandas as pd
import matplotlib.pyplot as plt

class Logger:
    def __init__(self):
        self.df = pd.DataFrame(columns=["generation", "max_fitness", "avg_fitness"])

    def log(self, generation, population):
        fitnesses = [b.fitness for b in population]
        self.df.loc[len(self.df)] = {
            "generation": generation,
            "max_fitness": max(fitnesses),
            "avg_fitness": sum(fitnesses) / len(fitnesses)
        }

    def save(self, path="results/log.csv"):
        self.df.to_csv(path, index=False)

    def plot_avg(self, path="results/avg_fitness_plot.png"):
        plt.figure(figsize=(10, 5))
        plt.plot(self.df["generation"], self.df["avg_fitness"], label="Average Fitness")
        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.title("Avg Fitness over Generations")
        plt.legend()
        plt.savefig(path)
        plt.close()

    def plot_max(self, path="results/max_fitness_plot.png"):
        plt.figure(figsize=(10, 5))
        plt.plot(self.df["generation"], self.df["max_fitness"], label="Max Fitness")
        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.title("Max Fitness over Generations")
        plt.legend()
        plt.savefig(path)
        plt.close()
