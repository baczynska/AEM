#!/usr/bin/env python3

import numpy as np
import math
import random
from decimal import localcontext, Decimal, ROUND_HALF_UP
import operator

vertex_num = 100
cycle_vertex_num = math.ceil(vertex_num / 2)
choosen_vertex = []
cycle_length = 0

distance_matrix = np.full((vertex_num, vertex_num), -1)
arr_of_vertex = []
idxs = np.arange(vertex_num)

distance_list = {}


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
        except:
            continue

        # arr_of_vertex[-1].show_vertex()


def fill_dictance_matrix():
    for idxA, first_vertex in enumerate(arr_of_vertex):
        for idxB, second_vertex in enumerate(arr_of_vertex):

            if idxA >= idxB:
                continue

            distance_matrix[idxA, idxB] = first_vertex.calculate_distance(second_vertex.x, second_vertex.y)
            distance_matrix[idxB, idxA] = distance_matrix[idxA, idxB]


def find_the_closest_to(vertex_id, distance_array):
    min_value = min(i for i in distance_array[:, vertex_id] if i > 0)
    # print(min_value)

    return list(distance_array[:, vertex_id]).index(min_value), min_value


def reset_for(vertex, distance_array):
    distance_array[:, vertex] = -1
    distance_array[vertex, :] = -1

    return distance_array


def create_distance_list():
    for x in range(vertex_num):
        distance_list[x] = sorted(range(len(distance_matrix[x, :])), key=lambda k: distance_matrix[x, k])


def find_the_closest_new_vertexes(current_vertexes):
    new_vertexes = []

    for v in current_vertexes:
        for n in distance_list[v]:
            if n not in current_vertexes:

                arr1 = current_vertexes.copy()
                arr1.insert(list(arr1).index(v), n)
                d1 = count_distance(arr1)

                arr2 = current_vertexes.copy()
                arr2.insert(list(arr2).index(v) + 1, n)
                d2 = count_distance(arr2)

                if d1 <= d2:
                    new_vertexes.append([n, v, d1])
                else:
                    new_vertexes.append([n, v, d2])

                break

    return new_vertexes


def count_distance(arry_with_vertexes):
    distance = 0
    for idx, vertex in enumerate(arry_with_vertexes):
        if vertex != arry_with_vertexes[-1]:
            distance += distance_matrix[vertex, arry_with_vertexes[idx + 1]]
        else:
            distance += distance_matrix[arry_with_vertexes[0], arry_with_vertexes[-1]]

    return distance


def greedy_nearest_neigh(first_vertex, distance_array):
    cycle_length = 0
    choosen_vertex.append(first_vertex)
    next_vertex = first_vertex
    for x in range(cycle_vertex_num - 1):
        new_vertex, distance = find_the_closest_to(next_vertex, distance_array)
        cycle_length += distance
        distance_array = reset_for(next_vertex, distance_array)
        next_vertex = new_vertex
        choosen_vertex.append(new_vertex)

    print("Lista wierzcholkow: ")
    print(choosen_vertex)
    print("Dlugosc cyklu:")
    print(count_distance(choosen_vertex))

    return cycle_length


def greedy_cycle(first_vertex, distance_array):
    choosen_vertex = []
    choosen_vertex.append(first_vertex)
    second_vertex, distance = find_the_closest_to(first_vertex, distance_array)
    choosen_vertex.append(second_vertex)
    create_distance_list()

    # wstawiam kolejne 48 wierzchołków
    for x in range(cycle_vertex_num - 2):
        the_best_option = None
        the_best_result_after_insert = None

        # iteruje po wierzchołkach i możliwych umiejscowieniach
        for free_vertex in range(vertex_num):
            if free_vertex not in choosen_vertex:
                for p in range(len(choosen_vertex)):
                    choosen_vertex_copy1 = choosen_vertex.copy()
                    choosen_vertex_copy1.insert(p + 1,free_vertex)
                    d = count_distance(choosen_vertex_copy1)
                    if (the_best_result_after_insert is None) or ( d < the_best_result_after_insert):
                        the_best_option = choosen_vertex_copy1.copy()
                        the_best_result_after_insert = d
                    else:
                        continue
        # print(the_best_option)
        choosen_vertex = the_best_option.copy()

    print("Lista wierzcholkow: ")
    print(choosen_vertex)
    print("Dlugosc cyklu:")
    print(count_distance(choosen_vertex))

    return cycle_length


def regret_heuristic(first_vertex, distance_array):
    choosen_vertex = []
    choosen_vertex.append(first_vertex)
    second_vertex, distance = find_the_closest_to(first_vertex, distance_array)
    choosen_vertex.append(second_vertex)

    # wstawiam kolejne 49 wierzchołków
    for x in range(cycle_vertex_num - 2):
        # vertex_id : [cost, place_to_insert]
        vertex_regret = {}

        # dla każdego jeszcze nie wstawionego wierzchołka
        for free_vertex in range(vertex_num):
            if free_vertex not in choosen_vertex:
                # place_to_insert : distance
                vertex_places = {}
                # w każde możliwe miejsce obecnego cyklu
                for i in range(len(choosen_vertex)):

                    choosen_vertex_local_copy = list(choosen_vertex.copy())
                    choosen_vertex_local_copy.insert(i + 1, free_vertex)
                    # print(choosen_vertex_local_copy)
                    vertex_places[i + 1] = count_distance(choosen_vertex_local_copy)
                v_p = sorted(vertex_places.items(), key=operator.itemgetter(1))
                # print(v_p)
                vertex_regret[free_vertex] = [int(v_p[1][1] - v_p[0][1]), v_p[0][0]]
        v_r = sorted(vertex_regret.items(), key=operator.itemgetter(1))
        # print(v_r)
        winner = v_r[-1]
        # print(winner)
        choosen_vertex.insert(int(winner[1][1]), int(winner[0]))

    print("Lista wierzcholkow: ")
    print(choosen_vertex)
    print("Dlugosc cyklu:")
    print(count_distance(choosen_vertex))

    return cycle_length

"""
    Wczytanie pliku do macierzy odległości
"""
load_instance("kroB100.tsp.txt")

"""
    Greedy - najbliższego sąsiada
"""
# for x in random.sample(list(idxs), 50):
#     fill_dictance_matrix()
#     working_distance_array = distance_matrix.copy()
#     choosen_vertex = []
#     cycle_length = greedy_nearest_neigh(x, working_distance_array)
#     print("Dlugosc cyklu: ", cycle_length)

"""
    Greedy - Cycle
"""
# for x in random.sample(list(idxs), 50):
#     choosen_vertex = []
#     fill_dictance_matrix()
#     greedy_cycle(x, distance_matrix)

"""
    Żal
"""
# for x in random.sample(list(idxs), 1):
#     print("First vertex: ", x)
#     choosen_vertex = []
#     fill_dictance_matrix()
#     distance_matrix_copy = distance_matrix.copy()
#     regret_heuristic(x, distance_matrix_copy)

"""
    Wszystkie algorytmy
"""
for x in random.sample(list(idxs), 100):
    print("First vertex: ", x)
    print("Algorytm NNG")
    fill_dictance_matrix()
    working_distance_array = distance_matrix.copy()
    choosen_vertex = []
    cycle_length = greedy_nearest_neigh(x, working_distance_array)
    print("Algorytm GCY")

    choosen_vertex = []
    fill_dictance_matrix()
    working_distance_array2 = distance_matrix.copy()
    greedy_cycle(x, working_distance_array2)
    print("Algorytm ŻALU")

    choosen_vertex = []
    fill_dictance_matrix()
    working_distance_array3 = distance_matrix.copy()
    regret_heuristic(x, working_distance_array3)
