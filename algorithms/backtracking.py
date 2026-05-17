import time
import math

def solve_bkt(dist_matrix, mode="first", time_limit=10.0, max_solutions=5):
    """
    TSP Backtracking solver.

    Args:
        dist_matrix: NxN list of lists (distances between cities)
        mode: "first" | "all" | "time" | "y_solutions"
        time_limit: seconds (used when mode="time")
        max_solutions: integer (used when mode="y_solutions")

    Returns:
        dict with keys: best_tour (list), best_cost (float),
                        solutions_found (int), elapsed (float),
                        all_solutions (list of dicts, optional)
    """
    n = len(dist_matrix)
    best = {"tour": None, "cost": math.inf}
    stats = {"solutions_found": 0, "start": time.perf_counter(), "stop": False, "all": []}

    def tour_cost(tour):
        return sum(dist_matrix[tour[i]][tour[(i+1) % n]] for i in range(n))

    def backtrack(path, visited, current_cost):
        if stats["stop"]:
            return
        if mode == "time" and (time.perf_counter() - stats["start"]) > time_limit:
            stats["stop"] = True
            return

        if len(path) == n:
            total = current_cost + dist_matrix[path[-1]][path[0]]
            stats["solutions_found"] += 1
            if total < best["cost"]:
                best["cost"] = total
                best["tour"] = path[:]
            if mode == "first":
                stats["stop"] = True
            elif mode == "y_solutions" and stats["solutions_found"] >= max_solutions:
                stats["stop"] = True
            if mode == "all":
                stats["all"].append({"tour": path[:], "cost": total})
            return

        for city in range(n):
            if not visited[city]:
                new_cost = current_cost + dist_matrix[path[-1]][city]
                if new_cost < best["cost"]:  # pruning
                    visited[city] = True
                    path.append(city)
                    backtrack(path, visited, new_cost)
                    path.pop()
                    visited[city] = False

    visited = [False] * n
    visited[0] = True
    backtrack([0], visited, 0)

    elapsed = time.perf_counter() - stats["start"]
    return {
        "best_tour": best["tour"] or [0],
        "best_cost": best["cost"],
        "solutions_found": stats["solutions_found"],
        "elapsed": elapsed,
        "all_solutions": stats["all"],
    }
