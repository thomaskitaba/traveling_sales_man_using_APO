#!/usr/bin/python3
import random

# Updated graph with distance and heuristic values
graph = {
    "Addis Ababa": {
        "Adama": {"distance": 598, "heuristic": 50},
        "Bahir Dar": {"distance": 225, "heuristic": 150},
        "Hawassa": {"distance": 700, "heuristic": 200},
        "Gondar": {"distance": 600, "heuristic": 250},
        "Mekele": {"distance": 900, "heuristic": 300},
    },
    "Adama": {
        "Hawassa": {"distance": 164, "heuristic": 150},
        "Addis Ababa": {"distance": 598, "heuristic": 50},
    },
    "Bahir Dar": {
        "Gondar": {"distance": 378, "heuristic": 350},
        "Mekele": {"distance": 644, "heuristic": 300},
        "Addis Ababa": {"distance": 225, "heuristic": 150},
        "Hawassa": {"distance": 800, "heuristic": 300},
    },
    "Hawassa": {
        "Adama": {"distance": 164, "heuristic": 150},
        "Addis Ababa": {"distance": 700, "heuristic": 200},
    },
    "Gondar": {
        "Mekele": {"distance": 273, "heuristic": 280},
        "Bahir Dar": {"distance": 378, "heuristic": 350},
        "Addis Ababa": {"distance": 600, "heuristic": 250},
    },
    "Mekele": {
        "Addis Ababa": {"distance": 447, "heuristic": 400},
        "Gondar": {"distance": 273, "heuristic": 280},
        "Bahir Dar": {"distance": 644, "heuristic": 300},
    },
}
graph = {
    "Addis Ababa": {
        "Adama": {"distance": 598, "heuristic": 50},
        "Bahir Dar": {"distance": 225, "heuristic": 150},
        "Hawassa": {"distance": 700, "heuristic": 200},
    },
    "Adama": {
        "Hawassa": {"distance": 164, "heuristic": 150},
        "Addis Ababa": {"distance": 598, "heuristic": 50},
    },
    "Bahir Dar": {
        "Addis Ababa": {"distance": 225, "heuristic": 150},
        "Hawassa": {"distance": 800, "heuristic": 300},
    },
    "Hawassa": {
        "Adama": {"distance": 164, "heuristic": 150},
        "Addis Ababa": {"distance": 700, "heuristic": 200},
    },
}

# Parameters
alpha = 1  # Importance of pheromone
beta = 2  # Importance of heuristic
evaporation_rate = 0.5  # Pheromone evaporation rate
num_ants = 10  # Number of ants
iterations = 50  # Number of iterations

# Initialize pheromones
pheromones = {node: {neighbor: 1.0 for neighbor in graph[node]} for node in graph}


def calculate_probabilities(current_node, visited, alpha, beta):
    """Calculate probabilities for choosing the next city."""
    probabilities = {}
    total = 0

    for neighbor, data in graph[current_node].items():
        if neighbor not in visited:
            pheromone = pheromones[current_node][neighbor] ** alpha
            heuristic = (1 / data["distance"]) ** beta
            probabilities[neighbor] = pheromone * heuristic
            total += probabilities[neighbor]

    # Normalize probabilities
    for neighbor in probabilities:
        probabilities[neighbor] /= total

    return probabilities


def choose_next_city(probabilities):
    """Choose the next city based on probabilities."""
    rand = random.random()
    cumulative = 0
    for city, probability in probabilities.items():
        cumulative += probability
        if rand <= cumulative:
            return city
    return random.choice(list(probabilities.keys()))


def construct_route(start):
    """Construct a route for an ant."""
    route = [start]
    visited = set(route)

    while len(visited) < len(graph):
        current_node = route[-1]
        probabilities = calculate_probabilities(current_node, visited, alpha, beta)

        if not probabilities:  # No valid moves
            break

        next_city = choose_next_city(probabilities)
        route.append(next_city)
        visited.add(next_city)

    # Return to start if possible
    if route[-1] in graph and start in graph[route[-1]]:
        route.append(start)

    return route


def update_pheromones(routes, evaporation_rate):
    """Update pheromones based on the constructed routes."""
    # Evaporate pheromones
    for node in pheromones:
        for neighbor in pheromones[node]:
            pheromones[node][neighbor] *= (1 - evaporation_rate)

    # Add new pheromones
    for route, distance in routes:
        pheromone_deposit = 1 / distance
        for i in range(len(route) - 1):
            current, next_node = route[i], route[i + 1]
            if next_node in pheromones[current]:
                pheromones[current][next_node] += pheromone_deposit


def calculate_route_distance(route):
    """Calculate the total distance of a route."""
    try:
        return sum(graph[route[i]][route[i + 1]]["distance"] for i in range(len(route) - 1))
    except KeyError as e:
        print(f"Missing edge: {e}. Route: {route}")
        return float('inf')  # Assign infinite cost for incomplete routes


def aco(graph, pheromones, alpha, beta, evaporation_rate, num_ants, iterations):
    """Main ACO algorithm."""
    best_route = None
    best_distance = float('inf')

    for _ in range(iterations):
        routes = []

        for _ in range(num_ants):
            start = random.choice(list(graph.keys()))
            route = construct_route(start)
            distance = calculate_route_distance(route)

            if distance < best_distance:
                best_route = route
                best_distance = distance

            routes.append((route, distance))

        update_pheromones(routes, evaporation_rate)

    return best_route, best_distance


# Run the ACO algorithm
best_route, best_distance = aco(graph, pheromones, alpha, beta, evaporation_rate, num_ants, iterations)
print("Best route:", best_route)
print("Best distance:", best_distance)
