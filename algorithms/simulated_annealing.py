import random
import math

def tour_cost(tour, dist_matrix):
    n = len(tour)
    return sum(dist_matrix[tour[i]][tour[(i+1)%n]] for i in range(n))

def solve_sa(dist_matrix, T_max=1000.0, T_min=0.01, alpha=0.995,
             iterations=10000, init_mode="nn", seed=42):
    """
    Simulated Annealing for TSP (2-opt neighbourhood).

    Args:
        T_max: initial temperature
        T_min: stopping temperature
        alpha: cooling rate (geometric: T *= alpha each step)
        iterations: max iterations
        init_mode: "nn" (nearest neighbour start) or "random"
        seed: random seed

    Returns:
        dict: best_tour, best_cost, cost_history (every 100 iters),
              temp_history, acceptance_history
    """
    import sys
    sys.path.insert(0, ".")
    from algorithms.nearest_neighbour import solve_nn

    random.seed(seed)
    n = len(dist_matrix)

    if init_mode == "nn":
        current_tour, _ = solve_nn(dist_matrix, start=0)
    else:
        current_tour = list(range(n))
        random.shuffle(current_tour)

    current_cost = tour_cost(current_tour, dist_matrix)
    best_tour = current_tour[:]
    best_cost = current_cost

    T = T_max
    cost_history = [current_cost]
    temp_history = [T]
    accepted = 0
    total = 0

    for it in range(iterations):
        if T < T_min:
            break
        i, j = sorted(random.sample(range(n), 2))
        new_tour = current_tour[:i] + current_tour[i:j+1][::-1] + current_tour[j+1:]
        new_cost = tour_cost(new_tour, dist_matrix)
        delta = new_cost - current_cost
        total += 1

        if delta <= 0 or random.random() < math.exp(-delta / T):
            current_tour = new_tour
            current_cost = new_cost
            accepted += 1
            if current_cost < best_cost:
                best_cost = current_cost
                best_tour = current_tour[:]

        T *= alpha
        if it % 100 == 0:
            cost_history.append(current_cost)
            temp_history.append(T)

    return {
        "best_tour": best_tour,
        "best_cost": best_cost,
        "cost_history": cost_history,
        "temp_history": temp_history,
        "acceptance_rate": accepted / total if total > 0 else 0,
    }
