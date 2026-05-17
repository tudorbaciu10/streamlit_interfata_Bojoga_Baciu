import time
import math

def solve_nn(dist_matrix, start=0):
    """Nearest Neighbour greedy heuristic. Returns (tour, cost)."""
    n = len(dist_matrix)
    visited = [False] * n
    tour = [start]
    visited[start] = True
    for _ in range(n - 1):
        last = tour[-1]
        nearest = min((dist_matrix[last][j], j) for j in range(n) if not visited[j])[1]
        tour.append(nearest)
        visited[nearest] = True
    cost = sum(dist_matrix[tour[i]][tour[(i+1)%n]] for i in range(n))
    return tour, cost

def solve_nn_multistart(dist_matrix):
    """Run NN from every city as start. Returns best (tour, cost, all_results)."""
    n = len(dist_matrix)
    results = []
    for s in range(n):
        tour, cost = solve_nn(dist_matrix, start=s)
        results.append({"start": s, "tour": tour, "cost": cost})
    best = min(results, key=lambda x: x["cost"])
    return best["tour"], best["cost"], results
