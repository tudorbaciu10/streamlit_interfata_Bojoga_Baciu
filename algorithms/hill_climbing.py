import random
import math

def two_opt_swap(tour, i, j):
    return tour[:i] + tour[i:j+1][::-1] + tour[j+1:]

def tour_cost(tour, dist_matrix):
    n = len(tour)
    return sum(dist_matrix[tour[i]][tour[(i+1)%n]] for i in range(n))

def solve_hc(dist_matrix, max_iterations=5000, restarts=3, seed=42):
    """
    Hill Climbing with 2-opt neighbourhood and random restarts.

    Returns dict: best_tour, best_cost, cost_history (list per restart),
                  iterations_per_restart (list)
    """
    random.seed(seed)
    n = len(dist_matrix)
    global_best_tour = None
    global_best_cost = math.inf
    all_cost_history = []

    for _ in range(restarts):
        current = list(range(n))
        random.shuffle(current)
        current_cost = tour_cost(current, dist_matrix)
        cost_history = [current_cost]
        improved = True

        iterations = 0
        while improved and iterations < max_iterations:
            improved = False
            for i in range(1, n - 1):
                for j in range(i + 1, n):
                    new_tour = two_opt_swap(current, i, j)
                    new_cost = tour_cost(new_tour, dist_matrix)
                    if new_cost < current_cost:
                        current = new_tour
                        current_cost = new_cost
                        improved = True
                        break
                if improved:
                    break
            cost_history.append(current_cost)
            iterations += 1

        all_cost_history.append(cost_history)
        if current_cost < global_best_cost:
            global_best_cost = current_cost
            global_best_tour = current[:]

    return {
        "best_tour": global_best_tour,
        "best_cost": global_best_cost,
        "cost_history": all_cost_history,
    }
