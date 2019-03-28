import numpy as np
import matplotlib.pyplot as plt
import sys
import networkx as nx
from copy import deepcopy
import random
import math

### Update values ###

# Use the A-matrix to find a consensus
# Returns number of iterations and final average

def find_consensus(A, values, threshold=0.00000000001):
    stddev = np.std(values) 

    iter = 0
    while (stddev > threshold):
        values = update_values(A, values)
        stddev = np.std(values)
        iter += 1
    
    avg = np.average(values)
    return iter, avg

# w(k + 1) = A * w(k)
def update_values(A, values):
    return np.matmul(A, values)

### Generating functions ###

def generate_pos(graph):
    return [(random.randint(0, 1000), random.randint(0, 1000)) for i in range(graph.number_of_nodes())]

def generate_all_edges(graph, A):
    n = graph.number_of_nodes()
    return [(i, j) for i in range(n) for j in range(i, n) if (A[i, j] == 0 and i != j)]

# Deprecated
def generate_all_edgepairs(n, A):
    all_edges = generate_all_edges(n, A)
    return [(e1, e2) for e1 in all_edges for e2 in all_edges if (e1 != e2)]

def generate_A(graph):
    n = graph.number_of_nodes()
    A = np.zeros((n, n))

    for i in range(n):
        A[i, i] = 1 / float((graph.degree(i)) + 1)

    for e in graph.edges():
        A[e[0], e[1]] = 1 / float(graph.degree(e[0]) + 1)
        A[e[1], e[0]] = 1 / float(graph.degree(e[1]) + 1)

    return A

def calc_distance(john, pos):
    return [np.linalg.norm(np.array(pos[v1]) - np.array(pos[v2])) for (v1, v2) in john.edges()]

def randomize_pos_and_cost(john):
    pos = generate_pos(john)
    distance = calc_distance(john, pos)
    nodes = [i for i in range(john.number_of_nodes())]

    distance = dict(zip(john.edges(), distance))
    pos = dict(zip(nodes, pos))

    nx.set_node_attributes(john, pos, 'pos')
    nx.set_edge_attributes(john, distance, 'distance')

### Update graph ###

def update_row(v, A, graph):
    degree = graph.degree(v)

    for n in graph.neighbors(v):
        A[v, n] = 1 / float(degree + 1)
    
    A[v, v] = 1 / float(degree + 1)

def add_edge(v1, v2, A_0, graph_0):
    # No side effects pls
    graph = deepcopy(graph_0)
    A = deepcopy(A_0)

    v1_pos = graph.node[v1]['pos']
    v2_pos = graph.node[v2]['pos']
    dist = np.linalg.norm(np.array(v1_pos) - np.array(v2_pos))
    graph.add_edge(v1, v2, distance = dist)
    
    update_row(v1, A, graph)
    update_row(v2, A, graph)

    return graph, A

### Cost functions ###

def get_total_cost(graph):
    total_cost = 0

    for (v1, v2) in graph.edges():
        cost = graph[v1][v2]['distance']
        total_cost += cost

    return total_cost

### Matrix functions ###

def sec_larg_eig(A):
    eig_list, _  = np.linalg.eig(A)
    return second_largest(eig_list)

### Finding best edge(s) ###

def find_best_edge(graph_0, A_0, depth=1, all_edges=None, min_eigen=1):
    best_graph = graph_0
    best_edge_s = None

    if (all_edges == None):
        all_edges = generate_all_edges(graph_0, A_0)

    for i, e in enumerate(all_edges):
        # add potential edge
        graph, A = add_edge(e[0], e[1], A_0, graph_0)

        if depth > 1 and i + 1 < len(all_edges):
            eig_value, graph, e2 = find_best_edge(graph, A, depth - 1, all_edges[i + 1:])
            
            # Debug statement
            if e2==None:
                print(all_edges)
                print(i)
            
            e2.append(e)
            e = e2
        else:
            eig_value = sec_larg_eig(A)

        if eig_value < min_eigen:
            min_eigen = eig_value
            best_graph = graph
            best_edge_s = e if type(e) == list else [e]

    return min_eigen, best_graph, best_edge_s

### Prints and plots ###

def print_graph(graph, edge=None):
    pos = nx.kamada_kawai_layout(graph)
    nx.draw_networkx_edges(graph, pos)

    if (edge != None):
        nx.draw_networkx_edges(graph, pos, edgelist=edge, edge_color='r')

    nx.draw_networkx_nodes(graph, pos)
    nx.draw_networkx_labels(graph, pos)
    plt.show()


### Useful stuff ###

def second_largest(l):
    largest = round(l[0], 5)
    largest2 = None

    for i in l[1:]:
        i = round(i, 5)
        if i > largest:
            largest2 = largest
            largest = i
        elif i > largest2 or largest2 == None:
            largest2 = i
    
    return largest2
