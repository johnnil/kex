import numpy as np
import matplotlib.pyplot as plt
import sys
import networkx as nx
from copy import deepcopy
import random
import math
import scipy

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

def generate_all_edges_c(graph, A):
    n = graph.number_of_nodes()
    return [(i, j) for i in range(n) for j in range(i, n) if (A[i, j] == 0 and i != j and get_dist(graph, i, j) < 1000)]

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

def calc_distance(graph, pos):
    #overhead cost of preparing any signal
    #overhead = 100
    return [np.linalg.norm(np.array(pos[v1]) - np.array(pos[v2])) for (v1, v2) in graph.edges()]

def get_dist(graph, v1, v2):
    v1_pos = graph.node[v1]['pos']
    v2_pos = graph.node[v2]['pos']
    return np.linalg.norm(np.array(v1_pos) - np.array(v2_pos))

def randomize_pos_and_cost(john, pos=None):
    if pos == None:
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

def remove_edge(v1, v2, A_0, graph_0):
    # No side effects pls
    graph = deepcopy(graph_0)
    A = deepcopy(A_0)

    graph.remove_edge(v1, v2)
    A[v1, v2] = 0
    A[v2, v1] = 0
    
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

def summarize(graph, A):
    return sec_larg_eig(graph, A) * get_total_cost(graph)

def total_energy(graph, A):
    #energy consumption of one iteration
    energy = get_total_cost(graph)
    error = 0.001
    eps = 0.0000000001
    eig = sec_larg_eig(graph, A)
    # if(eig == 0):
    #     # complete graph: only one iteration is needed
    #     return energy

    return energy * (math.log(error)/math.log(eig + eps))

### Matrix functions ###

def sec_larg_eig(graph, A):
    eig_list, _  = np.linalg.eig(A)

    return float(second_largest(eig_list))

### Prints and plots ###

def print_graph(graph, name, edge=None):
    pos = nx.kamada_kawai_layout(graph)
    nx.draw_networkx_edges(graph, pos)

    if (edge != None):
        nx.draw_networkx_edges(graph, pos, edgelist=edge, edge_color='r')

    nx.draw_networkx_nodes(graph, pos)
    nx.draw_networkx_labels(graph, pos)
    plt.axis('off')
    plt.savefig(name)
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
        elif largest2 == None or i > largest2:
            largest2 = i
    
    return largest2

def calc_diff(n1, n2, graph):
    a = len(list(graph.neighbors(n1)))
    b = len(list(graph.neighbors(n2)))
    return abs(a-b)