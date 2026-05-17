import random
import math
import numpy as np

def tour_cost(tour, dist_matrix):
    n = len(tour)
    return sum(dist_matrix[tour[i]][tour[(i+1)%n]] for i in range(n))

def ox_crossover(p1, p2):
    """Order Crossover (OX) - always produces valid permutation."""
    n = len(p1)
    cx1, cx2 = sorted(random.sample(range(n), 2))
    child = [-1] * n
    child[cx1:cx2] = p1[cx1:cx2]
    fill = [g for g in p2 if g not in child]
    idx = 0
    for i in range(n):
        if child[i] == -1:
            child[i] = fill[idx]; idx += 1
    return child

def swap_mutate(tour, rate):
    if random.random() < rate:
        i, j = random.sample(range(len(tour)), 2)
        tour[i], tour[j] = tour[j], tour[i]
    return tour

def solve_ga(dist_matrix, pop_size=80, n_generations=300,
             mutation_rate=0.3, elitism=2, selection="tournament",
             k_tournament=3, seed=42):
    """
    Genetic Algorithm for TSP with OX crossover + swap mutation.

    Returns:
        dict: best_tour, best_cost, convergence (list of best cost per gen),
              avg_fitness_history (list per gen)
    """
    random.seed(seed)
    n = len(dist_matrix)

    # Init population
    pop = [random.sample(range(n), n) for _ in range(pop_size)]

    def fitness(tour):
        return -tour_cost(tour, dist_matrix)  # maximise -> negate cost

    convergence = []
    avg_history = []

    for gen in range(n_generations):
        fitnesses = [fitness(ind) for ind in pop]
        best_idx = fitnesses.index(max(fitnesses))
        convergence.append(-fitnesses[best_idx])
        avg_history.append(-sum(fitnesses) / len(fitnesses))

        def tournament(k):
            candidates = random.sample(list(zip(fitnesses, pop)), k)
            return max(candidates, key=lambda x: x[0])[1]

        def roulette():
            shifted = [f - min(fitnesses) + 1e-6 for f in fitnesses]
            total = sum(shifted)
            r = random.uniform(0, total)
            acc = 0
            for f, ind in zip(shifted, pop):
                acc += f
                if acc >= r:
                    return ind
            return pop[-1]

        # Elitism
        elite_indices = sorted(range(len(fitnesses)), key=lambda i: fitnesses[i], reverse=True)[:elitism]
        new_pop = [pop[i][:] for i in elite_indices]

        while len(new_pop) < pop_size:
            if selection == "tournament":
                p1 = tournament(k_tournament)
                p2 = tournament(k_tournament)
            else:
                p1 = roulette()
                p2 = roulette()
            child = ox_crossover(p1, p2)
            child = swap_mutate(child, mutation_rate)
            new_pop.append(child)

        pop = new_pop

    fitnesses = [fitness(ind) for ind in pop]
    best_idx = fitnesses.index(max(fitnesses))
    best_tour = pop[best_idx]
    best_cost = -fitnesses[best_idx]

    return {
        "best_tour": best_tour,
        "best_cost": best_cost,
        "convergence": convergence,
        "avg_fitness_history": avg_history,
    }
