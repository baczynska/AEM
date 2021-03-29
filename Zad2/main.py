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

set100 = set(list(range(0,100)))

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
    if(position1 < position2):
        tmp = cycle[position1:position2]
        cycle = cycle[:position1] + tmp[::-1] + cycle[position2:]
    else:
        tmp = cycle[position2:position1]
        cycle = cycle[:position2] + tmp[::-1] + cycle[position1:]
    return cycle

def steepest_vertex(cycle, not_cycle):
    length = count_distance(cycle)
    best = cycle.copy()
    for id, x in enumerate(cycle):
        for idn in range(50):
            new_cycle = cycle.copy()
            change_vertex_set(new_cycle, not_cycle, id, idn)
            new_length = count_distance(new_cycle)
            if (new_length < length): 
                length = new_length
                best = new_cycle.copy()
            new_cycle = cycle.copy()
            swap_vertex(new_cycle, id, idn)
            new_length = count_distance(new_cycle)
            if (new_length < length): 
                length = new_length
                best = new_cycle.copy()
    return best, length

def steepest_edge(cycle, not_cycle):
    length = count_distance(cycle)
    best = cycle.copy()
    for id, x in enumerate(cycle):
        for idn in range(50):
            new_cycle = cycle.copy()
            change_vertex_set(new_cycle, not_cycle, id, idn)
            new_length = count_distance(new_cycle)
            if (new_length < length): 
                length = new_length
                best = new_cycle.copy()
            new_cycle = cycle.copy()
            new_cycle = swap_edge(new_cycle, id, idn).copy()
            new_length = count_distance(new_cycle)
            if (new_length < length): 
                length = new_length
                best = new_cycle.copy()
    return best, length

def greedy_vertex(cycle, not_cycle, method, randomx, randomy):
    length = count_distance(cycle)
    best = cycle.copy()
    if(method==1):
        new_cycle = cycle.copy()
        change_vertex_set(new_cycle, not_cycle, randomx, randomy)
        new_length = count_distance(new_cycle)
        if (new_length < length): 
            length = new_length
            best = new_cycle.copy()
    else:
        new_cycle = cycle.copy()
        swap_vertex(new_cycle, randomx, randomy)
        new_length = count_distance(new_cycle)
        if (new_length < length): 
            length = new_length
            best = new_cycle.copy()
    return best, length
    
def greedy_edge(cycle, not_cycle, method, randomx, randomy):
    length = count_distance(cycle)
    best = cycle.copy()
    if(method==1):
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

def steepest_vertex_whole(cycle, not_cycle, cycle_length):
    cycle, length2 = steepest_vertex(cycle, not_cycle)
    while(length2 < cycle_length):
        setcycle = set(cycle)
        cycle_length = length2
        not_cycle = list(set100.difference(setcycle))
        cycle, length2 = steepest_vertex(cycle, not_cycle)
    return cycle, length2

def steepest_edge_whole(cycle, not_cycle, cycle_length):
    cycle, length2 = steepest_edge(cycle, not_cycle)
    while(length2 < cycle_length):
        setcycle = set(cycle)
        cycle_length = length2
        not_cycle = list(set100.difference(setcycle))
        cycle, length2 = steepest_edge(cycle, not_cycle)
    return cycle, length2

def greedy_vertex_whole(cycle, not_cycle, cycle_length):
    length2 = cycle_length-1
    while(length2 < cycle_length):
        cycle_length = length2
        randomx = list(range(50))
        random.shuffle(randomx)
        randomy = list(range(50))
        random.shuffle(randomy)
        methods = [1, 2]
        random.shuffle(methods)
        m1 = methods[0]

        for x in randomx:
            for y in randomy:
                vcycle, length2 = greedy_vertex(cycle, not_cycle, m1, x , y)
                if length2 < cycle_length:
                    cycle = vcycle.copy()
                    setcycle = set(cycle)
                    not_cycle = list(set100.difference(setcycle))
                    break
            if length2 < cycle_length:
                break
        
        if(length2 == cycle_length):
            m2 = methods[1]
            for x in randomx:
                for y in randomy:
                    vcycle, length2 = greedy_vertex(cycle, not_cycle, m2, x, y)
                    if length2 < cycle_length:
                        cycle = vcycle.copy()
                        setcycle = set(cycle)
                        not_cycle = list(set100.difference(setcycle))
                        break
                if length2 < cycle_length:
                    break
    return cycle, length2

def greedy_edge_whole(cycle, not_cycle, cycle_length):
    length2 = cycle_length-1
    while(length2 < cycle_length):
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
                vcycle, length2 = greedy_edge(cycle, not_cycle, m1, x , y)
                if length2 < cycle_length:
                    cycle = vcycle.copy()
                    setcycle = set(cycle)
                    not_cycle = list(set100.difference(setcycle))
                    break
            if length2 < cycle_length:
                break
        
        if(length2 == cycle_length):
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
    cycle1 = list(range(0,100))
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

"""
#random
best = []
best_length = 999999
worst_length = 0
avg_length = 0

start = time.time()
while(1):
    cycle, not_cycle, cycle_length = generate_random_cycle()
    if(cycle_length<best_length):
        best_length = cycle_length
        best = cycle.copy()
    if(cycle_length>worst_length):
        worst_length = cycle_length
    avg_length = (avg_length+cycle_length)/2
    now = time.time()
    if(now - start > 15):
        break
print(best_length)
print(worst_length)
print(avg_length)
visualize(best, "random")
#generate initial instances
cycles = []
not_cycles = []
cycle_lengths = []
"""
#generate instances
for i in range(100):
    cycle1, not_cycle1, cycle_length1 = generate_random_cycle()
    cycles.append(cycle1)
    not_cycles.append(not_cycle1)
    cycle_lengths.append(cycle_length1)
    f = open("initial_instancesA.txt", "a")
    f.write(str(i) + ": " + str(cycles[i]) + "\n")
    f.write(str(cycle_lengths[i]) + "\n")

"""
#steepest vertex
best = []
best_length = 999999
worst_length = 0
avg_length = 0
best_time = 99999999
worst_time = 0
avg_time = 0

for i in range(100):
    cycle, not_cycle, cycle_length = cycles[i], not_cycles[i], cycle_lengths[i]
    tmpcycle = cycle.copy()
    tmpnotcycle = not_cycle.copy()
    start = time.time()
    result, length = steepest_vertex_whole(tmpcycle, tmpnotcycle, cycle_length)
    print(length)
    end = time.time()
    cur_time = end - start
    avg_time += cur_time
    avg_length += length
    if(length < best_length):
        best_length = length
        best = result.copy()
    if(length > worst_length):
        worst_length = length
    if(cur_time < best_time):
        best_time = cur_time
    if(cur_time > worst_time):
        worst_time = cur_time

f = open("steepest_vertex_resultA.txt", "w")
f.write("Best cycle length of steepest vertex:" + str(best_length) + "\n")
f.write("Worst cycle length of steepest vertex:" + str(worst_length) + "\n")
f.write("Average cycle length of steepest vertex:" + str(avg_length/100) + "\n")
f.write("Best time of steepest vertex:" + str(best_time) + "\n")
f.write("Worst time of steepest vertex:" + str(worst_time) + "\n")
f.write("Average time of steepest vertex:" + str(avg_time/100) + "\n")
visualize(best, "steepest_vertex")

#steepest edge
best = []
best_length = 999999
worst_length = 0
avg_length = 0
best_time = 99999999
worst_time = 0
avg_time = 0

for i in range(100):
    cycle, not_cycle, cycle_length = cycles[i], not_cycles[i], cycle_lengths[i]
    tmpcycle = cycle.copy()
    tmpnotcycle = not_cycle.copy()
    start = time.time()
    result, length = steepest_edge_whole(tmpcycle, tmpnotcycle, cycle_length)
    print(length)
    end = time.time()
    cur_time = end - start
    avg_time += cur_time
    avg_length += length
    if(length < best_length):
        best_length = length
        best = result.copy()
    if(length > worst_length):
        worst_length = length
    if(cur_time < best_time):
        best_time = cur_time
    if(cur_time > worst_time):
        worst_time = cur_time

f = open("steepest_edge_resultA.txt", "w")
f.write("Best cycle length of steepest edge:" + str(best_length) + "\n")
f.write("Worst cycle length of steepest edge:" + str(worst_length) + "\n")
f.write("Average cycle length of steepest edge:" + str(avg_length/100) + "\n")
f.write("Best time of steepest edge:" + str(best_time) + "\n")
f.write("Worst time of steepest edge:" + str(worst_time) + "\n")
f.write("Average time of steepest edge:" + str(avg_time/100) + "\n")
visualize(best, "steepest_edge")

#greedy vertex
best = []
best_length = 999999
worst_length = 0
avg_length = 0
best_time = 99999999
worst_time = 0
avg_time = 0

for i in range(100):
    cycle, not_cycle, cycle_length = cycles[i], not_cycles[i], cycle_lengths[i]
    tmpcycle = cycle.copy()
    tmpnotcycle = not_cycle.copy()
    start = time.time()
    result, length = greedy_vertex_whole(tmpcycle, tmpnotcycle, cycle_length)
    print(length)
    end = time.time()
    cur_time = end - start
    avg_time += cur_time
    avg_length += length
    if(length < best_length):
        best_length = length
        best = result.copy()
    if(length > worst_length):
        worst_length = length
    if(cur_time < best_time):
        best_time = cur_time
    if(cur_time > worst_time):
        worst_time = cur_time

f = open("greedy_vertex_resultA.txt", "w")
f.write("Best cycle length of greedy vertex:" + str(best_length) + "\n")
f.write("Worst cycle length of greedy vertex:" + str(worst_length) + "\n")
f.write("Average cycle length of greedy vertex:" + str(avg_length/100) + "\n")
f.write("Best time of greedy vertex:" + str(best_time) + "\n")
f.write("Worst time of greedy vertex:" + str(worst_time) + "\n")
f.write("Average time of greedy vertex:" + str(avg_time/100) + "\n")
visualize(best, "greedy_vertex")


#greedy edge
best = []
best_length = 999999
worst_length = 0
avg_length = 0
best_time = 99999999
worst_time = 0
avg_time = 0

for i in range(100):
    cycle, not_cycle, cycle_length = cycles[i], not_cycles[i], cycle_lengths[i]
    tmpcycle = cycle.copy()
    tmpnotcycle = not_cycle.copy()
    start = time.time()
    result, length = greedy_edge_whole(tmpcycle, tmpnotcycle, cycle_length)
    print(length)
    end = time.time()
    cur_time = end - start
    avg_time += cur_time
    avg_length += length
    if(length < best_length):
        best_length = length
        best = result.copy()
    if(length > worst_length):
        worst_length = length
    if(cur_time < best_time):
        best_time = cur_time
    if(cur_time > worst_time):
        worst_time = cur_time

f = open("greedy_edge_resultA.txt", "w")
f.write("Best cycle length of greedy edge:" + str(best_length) + "\n")
f.write("Worst cycle length of greedy edge:" + str(worst_length) + "\n")
f.write("Average cycle length of greedy edge:" + str(avg_length/100) + "\n")
f.write("Best time of greedy edge:" + str(best_time) + "\n")
f.write("Worst time of greedy edge:" + str(worst_time) + "\n")
f.write("Average time of greedy edge:" + str(avg_time/100) + "\n")
visualize(best, "greedy_edge")

"""