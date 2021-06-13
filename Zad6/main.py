#!/usr/bin/env python3

import numpy as np
import math
import random
from decimal import localcontext, Decimal, ROUND_HALF_UP
import operator
import matplotlib.pyplot as plt
import sys
import time

vertex_num = 100
cycle_vertex_num = math.ceil(vertex_num / 2)
choosen_vertex = []

distance_matrix = np.full((vertex_num, vertex_num), -1)
arr_of_vertex = []
idxs = np.arange(vertex_num)

set100 = set(list(range(0, 100)))

distance_list = {}
x_ = []
y_ = []


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

def swap_vertex(cycle, position1, position2):
    cycle[position1], cycle[position2] = cycle[position2], cycle[position1]
    return cycle

def swap_edge(cycle, position1, position2):
    if (position1 < position2):
        tmp = cycle[position1:position2]
        cycle = cycle[:position1] + tmp[::-1] + cycle[position2:]
    else:
        tmp = cycle[position2:position1]
        cycle = cycle[:position2] + tmp[::-1] + cycle[position1:]
    return cycle

def greedy_edge(cycle, not_cycle, method, randomx, randomy):
    length = count_distance(cycle)
    best = cycle.copy()
    if (method == 1):
        new_cycle = cycle.copy()
        change_vertex_set(new_cycle, not_cycle, randomx, randomy)
        new_length = count_distance(new_cycle)
        if (new_length < length):
            length = new_length
            best = new_cycle.copy()
    else:
        new_cycle = cycle.copy()
        new_cycle = swap_edge(new_cycle, randomx, randomy).copy()
        new_length = count_distance(new_cycle)
        if (new_length < length):
            length = new_length
            best = new_cycle.copy()
    return best, length

def greedy_edge_whole(cycle, not_cycle, cycle_length):
    length2 = cycle_length - 1
    while (length2 < cycle_length):
        cycle_length = length2
        randomx = list(range(50))
        random.shuffle(randomx)
        randomy = list(range(50))
        random.shuffle(randomy)
        methods = [1, 2]
        random.shuffle(methods)
        m1 = methods[0]
        m2 = methods[1]

        for x in randomx:
            for y in randomy:
                vcycle, length2 = greedy_edge(cycle, not_cycle, m1, x, y)
                if length2 < cycle_length:
                    cycle = vcycle.copy()
                    setcycle = set(cycle)
                    not_cycle = list(set100.difference(setcycle))
                    break
            if length2 < cycle_length:
                break

        if (length2 == cycle_length):
            for x in randomx:
                for y in randomy:
                    vcycle, length2 = greedy_edge(cycle, not_cycle, m2, x, y)
                    if length2 < cycle_length:
                        cycle = vcycle.copy()
                        setcycle = set(cycle)
                        not_cycle = list(set100.difference(setcycle))
                        break
                if length2 < cycle_length:
                    break
    return cycle, length2

def generate_random_cycle():
    cycle1 = list(range(0, 100))
    cycle = random.sample(cycle1, 50)
    setcycle = set(cycle)
    not_cycle = list(set100.difference(setcycle)).copy()
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

def check_similarityA(cycle1, cycle2):
    sum = 0
    for vertex in cycle1:
        if vertex in cycle2:
            sum +=1
    return sum

def make_edge_list(cycle):
    edges = []
    for i in range(len(cycle)-1):
        edges.append([cycle[i], cycle[i+1]])
    return edges

def check_similarityB(edges1, edges2):
    sum = 0
    for edge in edges1:
        if edge in edges2:
            sum +=1
    return sum


load_instance("kroB100.tsp.txt")
fill_distance_matrix()

# generate initial instances
cycles = []
not_cycles = []
cycle_lengths = []

for i in range(1000):
    cycle1, not_cycle1, cycle_length1 = generate_random_cycle()
    cycles.append(cycle1)
    not_cycles.append(not_cycle1)
    cycle_lengths.append(cycle_length1)

#greedy edge
best = []
best_length = 999999

results = []
lengths = []

for i in range(1000):
    cycle, not_cycle, cycle_length = cycles[i], not_cycles[i], cycle_lengths[i]
    tmpcycle = cycle.copy()
    tmpnotcycle = not_cycle.copy()

    result, length = greedy_edge_whole(tmpcycle, tmpnotcycle, cycle_length)
    print(length)
    results.append(result)
    lengths.append(length)

    if(length < best_length):
        best_length = length
        best = result.copy()

results.remove(best)
lengths.remove(best_length)

similarityToBestA = []
similarityToBestB = []

avgSimilarityA = []
avgSimilarityB = []

best_edges = make_edge_list(best)

edges_all = []

for i in results:
    edges_all.append(make_edge_list(i))

for i in results:
    similarityToBestA.append(check_similarityA(i, best))
    tmpres = results.copy()
    tmpres.remove(i)
    avg = 0
    for j in tmpres:
        avg += check_similarityA(i, j)
    avgSimilarityA.append(avg/len(tmpres))

    edges = edges_all[results.index(i)]

    avg = 0
    for j in tmpres:
        avg += check_similarityB(edges, edges_all[results.index(j)])
    avgSimilarityB.append(avg/len(tmpres))

    similarityToBestB.append(check_similarityB(edges, best_edges))

print(similarityToBestA)
print(similarityToBestB)
print(avgSimilarityA)
print(avgSimilarityB)

f = open("greedy_edge_resultB.txt", "w")
f.write("Wspólne wierzchołki z najlepszym rozwiązaniem: " + str(similarityToBestA) + "\n")
f.write("Wspólne krawędzie z najlepszym rozwiązaniem: " + str(similarityToBestB) + "\n")

f.write("Średnie podobieństwo wierzchołków do pozostałych rozwiązań: " + str(avgSimilarityA) + "\n")
f.write("Średnie podobieńśtwo krawędzi do pozostałych rozwiązań: " + str(avgSimilarityB) + "\n")
f.write("Współczynnik korelacji: " + str(np.corrcoef(avgSimilarityA, avgSimilarityB)))

plt.plot(lengths, avgSimilarityA, 'ro')
plt.show()
plt.plot(lengths, avgSimilarityB, 'ro')
plt.show()

