import math
from decimal import localcontext, Decimal, ROUND_HALF_UP
import time
import random
import numpy as np
import matplotlib.pyplot as plt

vertex_num = 200
cycle_vertex_num = math.ceil(vertex_num / 2)
choosen_vertex = []

distance_matrix = np.full((vertex_num, vertex_num), -1)
arr_of_vertex = []
idxs = np.arange(vertex_num)

set100 = set(list(range(0, 200)))

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


def generate_random_cycle():
    cycle1 = list(range(0, 200))
    cycle = random.sample(cycle1, 100)
    setcycle = set(cycle)
    not_cycle = list(set100.difference(setcycle)).copy()
    cycle_length = count_distance(cycle)
    return cycle, not_cycle, cycle_length


def count_distance(arry_with_vertexes):
    distance = 0
    for idx, vertex in enumerate(arry_with_vertexes):
        if vertex != arry_with_vertexes[-1]:
            distance += distance_matrix[vertex, arry_with_vertexes[idx + 1]]
        else:
            distance += distance_matrix[arry_with_vertexes[0], arry_with_vertexes[-1]]

    return distance


def steepest_edge_whole_kan(cycle):
    cycle_length = count_distance(cycle)
    cycle = steepest_edge_kan(cycle)
    length2 = count_distance(cycle)
    while length2 < cycle_length:
        cycle_length = length2
        cycle = steepest_edge_kan(cycle)
        length2 = count_distance(cycle)
    not_cycle = list(set100.difference(cycle)).copy()
    print(len(cycle) == 100 )
    return cycle, not_cycle, length2


def steepest_edge_kan(cycle):
    length = count_distance(cycle)
    search = True

    while search:
        search = False
        for id, x in enumerate(cycle):

            # print(distance_matrix[x])
            # print(sorted(range(len(distance_matrix[x])), key=lambda k: distance_matrix[x][k]))
            the_closest = sorted(range(len(distance_matrix[x])), key=lambda k: distance_matrix[x][k])[1:6]
            for nc in the_closest:
                # wprowadzenie krawedzi do rozwiazania
                if nc not in cycle:
                    setcycle = set(cycle)
                    not_cycle = list(set100.difference(setcycle))
                    new_cycle = cycle.copy()
                    change_vertex_set(new_cycle, not_cycle, (id + 1) % len(cycle), not_cycle.index(nc))
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


def rekombinacja_rodzicow(parents):
    parent1 = populacja[parents[0]][0]
    parent2 = populacja[parents[1]][0]
    intersected = list(set(parent1).intersection(parent2))
    diff = list(set(parent1).difference(parent2))
    random.shuffle(diff)
    new_child = []

    for i in range(len(parent1)):
        if parent1[i] in intersected:
            new_child.append(parent1[i])
        else:
            new_child.append(diff[0])
            diff.pop(0)

    not_cycle = list(set100.difference(new_child)).copy()
    cycle_length = count_distance(new_child)

    # print(f"************ {len(set(new_child))} ************")

    return [cycle_length, new_child, not_cycle]


### MAIN ###

load_instance("kroB200.tsp.txt")
fill_distance_matrix()

# generate initial instances
ROZMIAR_POPULACJI = 20
populacja = {}
bests = {}
worses = []
avgs = []

times = []

for _ in range(10):

    start = time.time()

    while len(populacja.keys()) < 20:
        cycle1, not_cycle1, cycle_length1 = generate_random_cycle()
        populacja[cycle_length1] = [cycle1, not_cycle1]

    for _ in range(100):

        # TAKE 2 RANDOM PARENTS
        arr_with_keys = list(populacja.keys())
        # print(sum(arr_with_keys))
        the_worse_result = max(arr_with_keys)
        parents_ids = random.sample(arr_with_keys, k=2)

        child_length, child_cycle, child_not_cycle = rekombinacja_rodzicow(parents_ids)
        # visualize(child_cycle, "child_cycle")

        # steepest edge, Kandydackie

        tmpcycle = child_cycle.copy()
        new_child_cycle, new_child_not_cycle, new_child_length = steepest_edge_whole_kan(tmpcycle)

        if new_child_length < the_worse_result and new_child_length not in populacja.keys():
            populacja.pop(the_worse_result)
            populacja[new_child_length] = [new_child_cycle, new_child_not_cycle]

    times.append(time.time() - start)

    the_best = min(list(populacja.keys()))
    the_worse = max(list(populacja.keys()))
    suma = sum(list(populacja.keys()))
    bests[the_best] = populacja[the_best]
    # visualize(populacja[the_best][0], f"{len(populacja[the_best][0])}")
    worses.append(the_worse)
    avgs.append(suma/ROZMIAR_POPULACJI)

the_best_length = min(list(bests.keys()))
the_worse_length = max(list(bests.keys()))

avg_length = sum(avgs)/len(avgs)

the_best = bests[the_best_length][0]

f = open("test.txt", "w")
f.write("Best cycle length of steepest edge:" + str(the_best_length) + "\n")
f.write("Worst cycle length of steepest edge:" + str(the_worse_length) + "\n")
f.write("Average cycle length of steepest edge:" + str(avg_length / 10) + "\n")
f.write("Best time of steepest edge:" + str(min(times)) + "\n")
f.write("Worst time of steepest edge:" + str(max(times)) + "\n")
f.write("Average time of steepest edge:" + str(sum(times) / 10) + "\n")

visualize(the_best, f"{the_best_length}")
