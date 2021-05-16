#!/usr/bin/env python3

import numpy as np
import math
import random
from decimal import localcontext, Decimal, ROUND_HALF_UP
import operator
import matplotlib.pyplot as plt
import sys
import time
import copy

vertex_num = 200
cycle_vertex_num = math.ceil(vertex_num / 2)
choosen_vertex = []

distance_matrix = np.full((vertex_num, vertex_num), -1)
arr_of_vertex = []
idxs = np.arange(vertex_num)

set200 = set(list(range(0, 200)))

distance_list = {}
x_ = []
y_ = []

def fill_dictance_matrix():
    for idxA, first_vertex in enumerate(arr_of_vertex):
        for idxB, second_vertex in enumerate(arr_of_vertex):

            if idxA >= idxB:
                continue

            distance_matrix[idxA, idxB] = first_vertex.calculate_distance(second_vertex.x, second_vertex.y)
            distance_matrix[idxB, idxA] = distance_matrix[idxA, idxB]

class Vertex:
    def __init__(self, idx, x, y):
        self.idx = idx - 1
        self.x = x
        self.y = y

    def show_vertex(self):
        print(f"Idx: {self.idx} ({self.x},{self.y})")

    def calculate_distance(self, second_x, second_y):
        with localcontext() as ctx:
            ctx.rounding = ROUND_HALF_UP
            return Decimal(math.sqrt((self.x - second_x) ** 2 + (self.y - second_y) ** 2)).to_integral_value()

def load_instance(instance_name):
    f = open(f"Dane/{instance_name}", "r")

    for line in f:

        idx, *ax = line.split(" ")
        if len(ax) != 2:
            continue

        try:
            arr_of_vertex.append(Vertex(int(idx), int(ax[0]), int(ax[1])))
            x_.append(int(ax[0]))
            y_.append(int(ax[1]))
        except:
            continue

def fill_distance_matrix():
    for idxA, first_vertex in enumerate(arr_of_vertex):
        for idxB, second_vertex in enumerate(arr_of_vertex):

            if idxA >= idxB:
                continue

            distance_matrix[idxA, idxB] = first_vertex.calculate_distance(second_vertex.x, second_vertex.y)
            distance_matrix[idxB, idxA] = distance_matrix[idxA, idxB]

def count_distance(arry_with_vertexes):
    distance = 0
    for idx, vertex in enumerate(arry_with_vertexes):
        if vertex != arry_with_vertexes[-1]:
            distance += distance_matrix[vertex, arry_with_vertexes[idx + 1]]
        else:
            distance += distance_matrix[arry_with_vertexes[0], arry_with_vertexes[-1]]

    return distance

def change_vertex_set(cycle, not_cycle, position1, position2):
    cycle[position1] = not_cycle[position2]
    return cycle

def swap_edge(cycle, position1, position2):
    new_cycle = cycle
    if position1 < position2:
        tmp = new_cycle[position1:position2]
        new_cycle = new_cycle[:position1] + tmp[::-1] + new_cycle[position2:]
    else:
        tmp = new_cycle[position2:position1]
        new_cycle = new_cycle[:position2] + tmp[::-1] + new_cycle[position1:]

    return cycle, new_cycle

def steepest_edge_kan(cycle):
    length = count_distance(cycle)
    search = True

    while search:
        search = False
        for id, x in enumerate(cycle):

            # print(distance_matrix[x])
            # print(sorted(range(len(distance_matrix[x])), key=lambda k: distance_matrix[x][k]))
            the_closest = sorted(range(len(distance_matrix[x])), key=lambda k: distance_matrix[x][k])[1:20]
            for nc in the_closest:
                # wprowadzenie krawedzi do rozwiazania
                if nc not in cycle:
                    setcycle = set(cycle)
                    not_cycle = list(set200.difference(setcycle))
                    new_cycle = cycle.copy()
                    change_vertex_set(new_cycle, not_cycle, (id + 1)%len(cycle), not_cycle.index(nc))
                    new_length = count_distance(new_cycle)

                    if new_length < length:
                        length = new_length
                        cycle = new_cycle.copy()
                        search = True

                if nc in cycle:
                    _, new_cycle = swap_edge(cycle, id, cycle.index(nc))
                    new_length = count_distance(new_cycle)

                    if new_length < length:
                        length = new_length
                        cycle = new_cycle.copy()
                        search = True

    return cycle

def check_possibilities_and_apply(cycle, length, LM_vertices, LM_edges):
    new_LM_edges = LM_edges.copy()
    new_LM_vertices = LM_vertices.copy()

    for (x_c, x_nc) in LM_vertices:

        if x_c in cycle and x_nc not in cycle:
            try:
                new_cycle = cycle.copy()
                change_vertex_set(new_cycle, not_cycle, new_cycle.index(x_c), not_cycle.index(x_nc))
                new_length = count_distance(new_cycle)

                if new_length < length:

                    length = new_length
                    cycle = new_cycle.copy()
                    return cycle, length, new_LM_vertices, new_LM_edges, True

                else:
                    del new_LM_vertices[(x_c, x_nc)]

            except:

                del new_LM_vertices[(x_c, x_nc)]

        else:
            del new_LM_vertices[(x_c, x_nc)]

    for (x_c, x_nc) in LM_edges:
        try:
            new_cycle = cycle.copy()
            old_cycle, new_cycle = swap_edge(new_cycle, new_cycle.index(x_c), new_cycle.index(x_nc))
            new_length = count_distance(new_cycle)

            if new_length < length:

                length = new_length
                cycle = new_cycle.copy()
                return cycle, length, new_LM_vertices, new_LM_edges, True

            else:
                del new_LM_edges[(x_c, x_nc)]
        except:
            # print("dell")
            del new_LM_edges[(x_c, x_nc)]

    return cycle, length, new_LM_vertices, new_LM_edges, False

def steepest_edge_whole_kan(cycle):
    cycle_length = count_distance(cycle)
    cycle = steepest_edge_kan(cycle)
    length2 = count_distance(cycle)
    while length2 < cycle_length:
        cycle_length = length2
        cycle = steepest_edge_kan(cycle)
        length2 = count_distance(cycle)
    return cycle, length2

def generate_random_cycle():
    cycle1 = list(range(0, 200))
    cycle = random.sample(cycle1, 100)
    setcycle = set(cycle)
    not_cycle = list(set200.difference(setcycle)).copy()
    cycle_length = count_distance(cycle)
    return cycle, not_cycle, cycle_length

def visualize(vertex_array, title):
    new_x, new_y = zip(*sorted(zip(x_, y_)))
    plt.plot(new_x, new_y, 'bo')

    x_c = []
    y_c = []
    vertex_array.append(vertex_array[0])
    for v in vertex_array:
        x_c.append(x_[v])
        y_c.append(y_[v])
    plt.plot(x_c, y_c)
    plt.title(title)
    plt.show()

def pertubation_1(cycle, not_cycle):

    for i in range(5):
        vertex1 = random.randint(0,99)
        vertex2 = random.randint(0,99)
        cycle = change_vertex_set(cycle, not_cycle, vertex1, vertex2).copy()
        not_cycle = list(set200.difference(set(cycle))).copy()

    return cycle, not_cycle

def find_the_closest_to(vertex_id, distance_array):
    min_value = min(i for i in distance_array[:, vertex_id] if i > 0)

    return list(distance_array[:, vertex_id]).index(min_value), min_value

def reset_for(vertex, distance_array):
    distance_array[:, vertex] = -1
    distance_array[vertex, :] = -1

    return distance_array

def greedy_nearest_neigh(cycle, first_vertex, distance_array):
    result = cycle.copy()
    next_vertex = first_vertex
    for x in range(20):
        new_vertex, distance = find_the_closest_to(next_vertex, distance_array)
        distance_array = reset_for(next_vertex, distance_array)
        next_vertex = new_vertex
        result.append(new_vertex)

    return result

def pertubation_2(cycle, not_cycle, distance_array):
    new_cycle = []

    starting_point = random.randint(1, 79)
    destroyed = cycle[:starting_point] + cycle[starting_point+20:]

    new_cycle = greedy_nearest_neigh(cycle[:starting_point], cycle[starting_point-1], distance_array) + cycle[starting_point+20:]
    not_cycle = set200.difference(set(new_cycle)).copy()
    
    return new_cycle, not_cycle


load_instance("kroA200.tsp.txt")
fill_distance_matrix()

msls_results = []
msls_avg = 0
msls_min = 0
msls_max = 0
best_time = 99999999
worst_time = 0
avg_time = 0

for x in range(10):
    # generate initial instances
    cycles = []
    not_cycles = []
    cycle_lengths = []
    for i in range(100):
        cycle1, not_cycle1, cycle_length1 = generate_random_cycle()
        cycles.append(cycle1)
        not_cycles.append(not_cycle1)
        cycle_lengths.append(cycle_length1)

    best_length = 999999

    #MSLS
    start = time.time()
    for i in range(100):
        cycle, not_cycle, cycle_length = cycles[i], not_cycles[i], cycle_lengths[i]
        tmpcycle = cycle.copy()
        result, length = steepest_edge_whole_kan(tmpcycle)       
        if length < best_length:
            best_length = length
            best = result.copy()

    end = time.time()
    cur_time = end - start

    avg_time += cur_time 
    print(best_length)
    msls_results.append(best_length)

avg_time = avg_time/10

msls_avg = sum(msls_results)/len(msls_results)
msls_max = max(msls_results)
msls_min = min(msls_results)

visualize(best, "MSLS")

f = open("resultA.txt", "w")
f.write("Best cycle length of MSLS: " + str(msls_min) + "\n")
f.write("Worst cycle length of MSLS: " + str(msls_max) + "\n")
f.write("Average cycle length of MSLS: " + str(msls_avg) + "\n")

ils1_results = []
ils1_avg = 0
ils1_min = 0
ils1_max = 0

#ILS1
for x in range(10):
    best_length = 999999
    end = 0
    start = time.time()

    cycle, not_cycle, cycle_length = generate_random_cycle()
    tmpcycle = cycle.copy()
    result, best_length = steepest_edge_whole_kan(tmpcycle)

    while end < avg_time:
        cycle_y, not_cycle_y = pertubation_1(cycle, not_cycle)
        tmpcycle = cycle_y.copy()
        result, length = steepest_edge_whole_kan(tmpcycle)

        if length < best_length:
            best_length = length
            best = result.copy()
            cycle = tmpcycle.copy()
            not_cycle = not_cycle_y.copy()

        end = time.time() - start
    print(best_length)
    ils1_results.append(best_length)

visualize(best, "ILS1")

ils1_avg = sum(ils1_results)/len(ils1_results)
ils1_max = max(ils1_results)
ils1_min = min(ils1_results)

f.write("Best cycle length of ILS1: " + str(ils1_min) + "\n")
f.write("Worst cycle length of ILS1: " + str(ils1_max) + "\n")
f.write("Average cycle length of ILS1: " + str(ils1_avg) + "\n")

ils2_results = []
ils2_avg = 0
ils2_min = 0
ils2_max = 0

#ILS2
for x in range(10):
    best_length = 999999
    end = 0
    start = time.time()

    cycle, not_cycle, cycle_length = generate_random_cycle()
    tmpcycle = cycle.copy()
    result, best_length = steepest_edge_whole_kan(tmpcycle)

    while end < avg_time:
        fill_dictance_matrix()
        working_distance_array = distance_matrix.copy()
        cycle_y, not_cycle_y = pertubation_2(cycle, not_cycle, working_distance_array)
        tmpcycle = cycle_y.copy()
        result, length = steepest_edge_whole_kan(tmpcycle)

        if length < best_length:
            best_length = length
            best = result.copy()
            cycle = tmpcycle.copy()
            not_cycle = not_cycle_y.copy()

        end = time.time() - start
    print(best_length)
    ils2_results.append(best_length)

ils2_avg = sum(ils2_results)/len(ils2_results)
ils2_max = max(ils2_results)
ils2_min = min(ils2_results)

visualize(best, "ILS2")

f.write("Best cycle length of ILS2: " + str(ils2_min) + "\n")
f.write("Worst cycle length of ILS2: " + str(ils2_max) + "\n")
f.write("Average cycle length of ILS2: " + str(ils2_avg) + "\n")

#ILS2A

ils2a_results = []
ils2a_avg = 0
ils2a_min = 0
ils2a_max = 0

for x in range(10):
    best_length = 999999
    end = 0
    start = time.time()

    cycle, not_cycle, cycle_length = generate_random_cycle()

    while end < avg_time:
        fill_dictance_matrix()
        working_distance_array = distance_matrix.copy()
        cycle_y, not_cycle_y = pertubation_2(cycle, not_cycle, working_distance_array)
        length = count_distance(cycle_y)

        if length < best_length:
            best_length = length
            best = result.copy()
            cycle = cycle_y.copy()
            not_cycle = not_cycle_y.copy()

        end = time.time() - start
    print(best_length)
    ils2a_results.append(best_length)

ils2a_avg = sum(ils2a_results)/len(ils2a_results)
ils2a_max = max(ils2a_results)
ils2a_min = min(ils2a_results)

visualize(best, "ILS2a")

f.write("Best cycle length of ILS2a: " + str(ils2a_min) + "\n")
f.write("Worst cycle length of ILS2a: " + str(ils2a_max) + "\n")
f.write("Average cycle length of ILS2a: " + str(ils2a_avg) + "\n")