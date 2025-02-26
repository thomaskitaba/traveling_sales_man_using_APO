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
        "Bahir Dar": {"distance": 250},  # Added
        "Hawassa": {"distance": 150},   # Standardized to 150
    },
    "Bahir Dar": {
        "Addis Ababa": {"distance": 150},
        "Adama": {"distance": 250},     # Added
        "Hawassa": {"distance": 200},
    },
    "Hawassa": {
        "Addis Ababa": {"distance": 175},
        "Adama": {"distance": 150},     # Standardized to 150
        "Bahir Dar": {"distance": 200},
    },
}
iterations = 50 
m = len(list(graph.keys())) # number_of_ants
alpha = 1
beta = 2 
evaporation_rate = 0.5 

# print(f"number_of_ants should be the sampe as : {m}")

paths = []  # structure  [([], int)]  means [(path, distance)]
max_distance = float("-inf")
routes = []
distance = 0
best_path = []
best_distanse = float("inf")
pheromones = { node: {adjesent: 1.0 for adjesent in neighbor.keys()} for node, neighbor in graph.items()}
# print(pheromones) #test Print


def calculate_probabilities(current_node, visited):
    probabilities = {}
    
    for neighbor in graph.get(current_node, []):
        
        # print(neighbor)
        # probablity = taw ** alpha  * raw  ** beta / sum of all .. 
        taw = pheromones[current_node][neighbor] ** alpha
        raw = 1/ (graph[current_node][neighbor]["distance"]) ** beta
        # total += graph[current_node][neighbor]["distance"]
        desire = taw * raw
        probabilities[neighbor] = desire
            
        # calculate probablity beteween city current_node and current neighbor
    total = sum(list(probabilities.values()))
    if total == 0:
        return probabilities
    # Normalize the probablity dictinary
    for node, value in probabilities.items():
        probabilities[node] = value/total

    
    
    return probabilities

def select_next_city_randomly(probablity_to_other_cities):
    random_number = random.random()   # generates randome number from 0 to 1

    # sort(probablity_to_other_cities)
    sorted_probablities = sorted(probablity_to_other_cities.items(), key = lambda x: x[1])
    # print(f"sorted_probablity: {sorted_probablities}")
   
    sorted_probablities_list = list(sorted(probablity_to_other_cities.items(), key = lambda x: x[1]))
    probabilities_list = list(sorted(probablity_to_other_cities.values(), key = lambda x: x))
    
    # create cummilateive probablity 
    for i in range(1, len( probabilities_list)):
         probabilities_list[i] =  probabilities_list[i] +  probabilities_list[i - 1]
    index_of_city_choice = 0
    
    lower_bound = 0
    for i in range(len( probabilities_list)):
        if random_number > lower_bound and random_number <= probabilities_list[i]:
            index_of_city_choice = i 
            break
        lower_bound = probabilities_list[i]
    # return key (chosen city)  from sorted_probablity_list
    
    chosen_city = sorted_probablities_list[index_of_city_choice][0]
    # print(f"CHOSEN CITY: {chosen_city}  random_number_value= {random_number}")
    # print(f"sorted probablity list tuple: {probabilities_list}")
    return chosen_city
    
def construct_path(graph, start):
    route = [start]
    visited = set()
    visited.add(start)
    # print(route, visited)
    # until all nodes are visited
    distance = 0
    
    while len(visited) < len(graph.keys()):
        
        # calculate probablity
        probablity_to_other_cities = calculate_probabilities(route[-1], visited)
        unvisited_probabilities = {city: prob for city, prob in probablity_to_other_cities.items() if city not in visited}
        if not unvisited_probabilities:
            break
        # chose the a city based on the probablity
        next_city = select_next_city_randomly(unvisited_probabilities)
        route.append(next_city)
        visited.add(next_city)
    
    return  route
def calculate_route_distance(path):
    distance = 0
    for i in range(len(path) - 1):
        distance += graph[path[i]][path[i+1]]["distance"]
    # print(distance)
    return distance

def add_phrmone_by_single_ant(ant_path_info):
    path = ant_path_info[0]
    distance = ant_path_info[1]
    
    for city, neighbor in pheromones.items():
        for name, phermone in neighbor.items():
            if name in path:
                pheromones[city][name] += 1 / distance
                
def global_phermone_update(paths):
    # sumation_of_all_pheromone = list(sorted(pheromones.items(), key = lambda x: x[1]))
    path = paths[0][0]
    distance = paths[1]
    sumation_of_all_pheromones = 0
    for key, neighbor in pheromones.items():
        for city in neighbor.values():
            sumation_of_all_pheromones += 1
    # print(f"sum of all phermones:- {sumation_of_all_pheromones}")
    for i in range(len(path) - 1):
        pheromones[path[i]][path[i + 1]] = (1 - evaporation_rate) * pheromones[path[i]][path[i + 1]] + sumation_of_all_pheromones
    # print(pheromones)
# launch ants from random location
for i in range(iterations):
    # best_distanse = float("inf")
    start = random.choice(list(graph.keys()))
    # if not paths:
    #     start = random.choice(list(graph.keys()))
    # else:
    #     start = paths[-1][0][-1]
    # print(start)
    for k in range(len(graph)):
        # construct path   return path and the assosiated distance
        path = construct_path(graph, start)

        distance = calculate_route_distance(path)
        paths.append((path, distance))
        # add phermone for a single ant journey
        add_phrmone_by_single_ant((path, distance))
        
        if distance < best_distanse:
            best_path = path
            best_distance = distance
       
        # update phermone after all the ants finish their path
        
    global_phermone_update(paths)
    
print(best_path, best_distance)
# print (f"=========== {best_path}, {best_distance}")     
    
print(pheromones)