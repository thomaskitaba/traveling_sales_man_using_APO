#!/usr/bin/python3
import random


graph = {
    "Addis Ababa": {
        "Adama": {"distance": 125},
        "Bahir Dar": {"distance": 150},
        "Hawassa": {"distance": 175},
    },
    "Adama": {
        "Addis Ababa": {"distance": 125},
        "Bahir Dar": {"distance": 250},
        "Hawassa": {"distance": 150},  
    },
    "Bahir Dar": {
        "Addis Ababa": {"distance": 150},
        "Adama": {"distance": 250},     
        "Hawassa": {"distance": 200},
    },
    "Hawassa": {
        "Addis Ababa": {"distance": 175},
        "Adama": {"distance": 150},    
        "Bahir Dar": {"distance": 200},
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
            # genteral formula: probablity = taw ** alpha  * raw  ** beta / sum of all .. 
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
    # generate random number from 0 to 1
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
    # loop until all cities in the graph are visited
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
        # print(graph[route[i]][route[i + 1]]["distance"])
        return sum(graph[route[i]][route[i + 1]]["distance"] for i in range(len(route) - 1))
    except KeyError as e:
        print(f"Missing edge: {e}. Route: {route}")
        return float('inf')  # Assign infinite cost for incomplete routes

def aco(graph, pheromones, alpha, beta, evaporation_rate, num_ants, iterations):
    """Main ACO algorithm."""
    best_route = None
    best_distance = float('inf')

    for _ in range(iterations): # all ants will be launched iteration times 
        routes = []
        for _ in range(num_ants):  # number of ants is recomended to be equal with number of cities
            start = random.choice(list(graph.keys()))
            route = construct_route(start) # path created by a single ant
            distance = calculate_route_distance(route) # distance covered by the ant along the path
            if distance < best_distance:
                best_route = route
                best_distance = distance
            routes.append((route, distance))
        update_pheromones(routes, evaporation_rate) # phermone will be updated based on phermone left by ants and rate of evaportaion
    return best_route, best_distance
# Run the ACO algorithm
best_route, best_distance = aco(graph, pheromones, alpha, beta, evaporation_rate, num_ants, iterations)
print("Best route:", best_route)
print("Best distance:", best_distance)

