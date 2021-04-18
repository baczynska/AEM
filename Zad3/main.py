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


def swap_edge(cycle, position1, position2):
    new_cycle = copy.deepcopy(cycle)
    if position1 < position2:
        tmp = new_cycle[position1:position2]
        new_cycle = new_cycle[:position1] + tmp[::-1] + new_cycle[position2:]
    else:
        tmp = new_cycle[position2:position1]
        new_cycle = new_cycle[:position2] + tmp[::-1] + new_cycle[position1:]

    return cycle, new_cycle


def steepest_edge_LM(cycle, not_cycle, dict_moves_verti=None, dict_moves_edges=None,
                     dict_moves_tested_verti_check=None, dict_moves_tested_edges_check=None, first=False):
    # sprawdzam poczatkowa dlugosc cyklu,
    # dla każdego wierzchołku w cyklu, wymieniam go na każdy wierzchołek z poza cyklu

    dict_moves_tested_verti = {}
    dict_moves_tested_edges = {}

    if first:
        dict_moves_verti = {}
        dict_moves_edges = {}

    length = count_distance(cycle)
    for id, x in enumerate(cycle):
        for idn in range(50):
            # poza cyklem
            if first or (x, not_cycle[idn]) not in dict_moves_tested_verti_check:
                setcycle = set(cycle)
                not_cycle = list(set100.difference(setcycle))
                new_cycle = cycle.copy()
                change_vertex_set(new_cycle, not_cycle, id, idn)
                new_length = count_distance(new_cycle)
                dict_moves_tested_verti[(x, not_cycle[idn])] = True
                dict_moves_tested_verti[(not_cycle[idn], x)] = True

                if new_length < length:
                    dict_moves_verti[(x, not_cycle[idn])] = length - new_length
                    # length = new_length
                    # best = new_cycle.copy()

            # wewnatrz
            if first or (x, cycle[idn]) not in dict_moves_tested_edges_check:
                new_cycle2 = cycle.copy()
                new_cycle2, count_len = swap_edge(new_cycle2, id, idn)
                new_length = count_distance(count_len)
                dict_moves_tested_edges[(x, cycle[idn])] = True
                dict_moves_tested_edges[(cycle[idn], x)] = True

                if new_length < length:
                    dict_moves_edges[(x, cycle[idn])] = length - new_length
                    # length = new_length
                    # best = new_cycle.copy()

    return dict(sorted(dict_moves_verti.items(), key=lambda item: item[1], reverse=True)), \
           dict(sorted(dict_moves_edges.items(), key=lambda item: item[1], reverse=True)), \
           dict_moves_tested_verti, dict_moves_tested_edges


def steepest_edge_kan(cycle):

    length = count_distance(cycle)
    search = True

    while search:
        search = False
        for id, x in enumerate(cycle):

            # print(distance_matrix[x])
            # print(sorted(range(len(distance_matrix[x])), key=lambda k: distance_matrix[x][k]))
            the_closest = sorted(range(len(distance_matrix[x])), key=lambda k: distance_matrix[x][k])[1:]
            for nc in the_closest:
                # wprowadzenie krawedzi do rozwiazania
                if nc not in cycle:
                    setcycle = set(cycle)
                    not_cycle = list(set100.difference(setcycle))
                    new_cycle = cycle.copy()
                    change_vertex_set(new_cycle, not_cycle, (id + 1)%len(cycle), not_cycle.index(nc))
                    new_length = count_distance(new_cycle)

                    if new_length < length:
                        length = new_length
                        cycle = new_cycle.copy()
                        search = True

                    _, new_cycle = swap_edge(new_cycle, id, new_cycle.index(nc))
                    new_length = count_distance(new_cycle)

                    if new_length < length:
                        length = new_length
                        cycle = new_cycle.copy()
                        search = True

    return cycle


def steepest_edge_whole_LM(cycle, length):
    search = True
    first = True
    while search:
        setcycle = set(cycle)
        not_cycle = list(set100.difference(setcycle))
        if first:
            dict_moves_verti, dict_moves_edges, tested_verti, tested_edges = \
                steepest_edge_LM(cycle, not_cycle, first=True)
        else:
            dict_moves_verti, dict_moves_edges, tested_verti, tested_edges \
                = steepest_edge_LM(cycle, not_cycle, dict_moves_verti, dict_moves_edges, tested_verti, tested_edges)
        cycle, length, dict_moves_verti, dict_moves_edges, search = \
            check_possibilities_and_apply(cycle, length, dict_moves_verti, dict_moves_edges)
        first = False
    return cycle, length


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
                    # print(new_cycle)

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
            # print("succ")
            new_length = count_distance(new_cycle)

            if new_length < length:
                # print("yess edge")

                length = new_length
                cycle = new_cycle.copy()
                return cycle, length, new_LM_vertices, new_LM_edges, True

            else:
                del new_LM_edges[(x_c, x_nc)]
        except:
            # print("dell")
            del new_LM_edges[(x_c, x_nc)]

    # print(length)

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


load_instance("kroA100.tsp.txt")
fill_distance_matrix()

# generate initial instances
cycles = []
not_cycles = []
cycle_lengths = []

for i in range(100):
    cycle1, not_cycle1, cycle_length1 = generate_random_cycle()
    cycles.append(cycle1)
    not_cycles.append(not_cycle1)
    cycle_lengths.append(cycle_length1)
    f = open("initial_instancesA.txt", "a")
    f.write(str(i) + ": " + str(cycles[i]) + "\n")
    f.write(str(cycle_lengths[i]) + "\n")

# steepest edge, LM
# best = []
# best_length = 999999
# worst_length = 0
# avg_length = 0
# best_time = 99999999
# worst_time = 0
# avg_time = 0
#
# for i in range(100):
#     print("************" + str(i) + "***************")
#     cycle, not_cycle, cycle_length = cycles[i], not_cycles[i], cycle_lengths[i]
#     tmpcycle = cycle.copy()
#     start = time.time()
#     result, length = steepest_edge_whole_LM(tmpcycle, cycle_length)
#     # print(length)
#     print(result)
#     end = time.time()
#     cur_time = end - start
#     avg_time += cur_time
#     avg_length += length
#     if length < best_length:
#         best_length = length
#         best = result.copy()
#     if length > worst_length:
#         worst_length = length
#     if cur_time < best_time:
#         best_time = cur_time
#     if cur_time > worst_time:
#         worst_time = cur_time
#
# f = open("steepest_edge_resultA_LM.txt", "w")
# f.write("Best cycle length of steepest edge:" + str(best_length) + "\n")
# f.write("Worst cycle length of steepest edge:" + str(worst_length) + "\n")
# f.write("Average cycle length of steepest edge:" + str(avg_length / 100) + "\n")
# f.write("Best time of steepest edge:" + str(best_time) + "\n")
# f.write("Worst time of steepest edge:" + str(worst_time) + "\n")
# f.write("Average time of steepest edge:" + str(avg_time / 100) + "\n")
# visualize(best, "steepest_edge")

# steepest edge, Kandydackie
best = []
best_length = 999999
worst_length = 0
avg_length = 0
best_time = 99999999
worst_time = 0
avg_time = 0

for i in range(100):
    print("************" + str(i) + "***************")
    cycle, not_cycle, cycle_length = cycles[i], not_cycles[i], cycle_lengths[i]
    # visualize(cycle, "steepest_edge")
    tmpcycle = cycle.copy()
    start = time.time()
    fill_distance_matrix()
    result, length = steepest_edge_whole_kan(tmpcycle)
    # print(length)
    print(result)
    end = time.time()
    cur_time = end - start
    avg_time += cur_time
    avg_length += length
    if length < best_length:
        best_length = length
        best = result.copy()
    if length > worst_length:
        worst_length = length
    if cur_time < best_time:
        best_time = cur_time
    if cur_time > worst_time:
        worst_time = cur_time

f = open("steepest_edge_resultA_kan.txt", "w")
f.write("Best cycle length of steepest edge:" + str(best_length) + "\n")
f.write("Worst cycle length of steepest edge:" + str(worst_length) + "\n")
f.write("Average cycle length of steepest edge:" + str(avg_length / 100) + "\n")
f.write("Best time of steepest edge:" + str(best_time) + "\n")
f.write("Worst time of steepest edge:" + str(worst_time) + "\n")
f.write("Average time of steepest edge:" + str(avg_time / 100) + "\n")
visualize(best, "steepest_edge")
