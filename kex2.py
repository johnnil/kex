import numpy as np
import matplotlib.pyplot as plt
import sys
import networkx as nx
from copy import deepcopy
import random

#####
hossein = nx.Graph()
hossein.add_edges_from([(0,1), (2,1), (1,3), (3,4), (3,5)])
#####

#####
emptyG = nx.Graph()
emptyG.add_nodes_from(range(6))
#####

def update_row(v, A, graph):
    degree = graph.degree(v)
    for n in graph.neighbors(v):
        A[v, n] = 1 / float(degree + 1)
    
    A[v, v] = 1 / float(degree + 1)

def add_edge(v1, v2, A, graph):
    graph.add_edge(v1, v2)
    update_row(v1, A, graph)
    update_row(v2, A, graph)


def generateA(graph):
    n = graph.number_of_nodes()
    A = np.zeros((n, n))

    for i in range(n):
        A[i, i] = 1 / float((graph.degree(i)) + 1)

    for e in graph.edges():
        A[e[0], e[1]] = 1 / float(graph.degree(e[0]) + 1)
        A[e[1], e[0]] = 1 / float(graph.degree(e[1]) + 1)

    return A

def find_consensus(A, values):
    avg = np.average(values)
    stddev = np.std(values)
    stddevs = [stddev]

    while (stddev > 0.01):
        values = update_values(A, values)
        stddev = np.std(values)
        stddevs.append(stddev)
    
    #print(values)
    #print(iter)
    return stddevs


def update_values(A, values):
    return np.matmul(A, values)

def plot_consensus_curve(result, iter):
    plt.plot(iter, result)
    plt.show()

def main_helper(graph, A):
    values = [i for i in range(6)]
    result = find_consensus(A, values)
    iterations = [i for i in range(len(result))]
    plot_consensus_curve(result, iterations)

def main():
    A = generateA(hossein)
    #main_helper(hossein, A)
    best_edge(hossein, A)
    #add_edge(0, 5, A, hossein)
    #main_helper(hossein, A)
    #best_two(hossein, A)


def getA():
    A = generateA(hossein)
    return A

def rand_val(n):
    return [random.randrange(n) for x in range(6)]

def generate_all_edges(n, A):
    return [(i, j) for i in range(n) for j in range(i, n) if (A[i, j] == 0 and i != j)]

def best_edge(graph, A):
    n = graph.number_of_nodes()
    miniter = 1001 # pseudo max integer
    bestEdge = ()
    alles = generate_all_edges(n, A)
    for e in alles:
        # Save restore point
        B = deepcopy(A)
        add_edge(e[0], e[1], A, graph)
        iter = 0

        for x in range(200):
            values = rand_val(10)
            iter += len(find_consensus(A, values))
        
        iter = iter / float(200)
        #iter = len(stddevs)
        #iterations = [k for k in range(iter)]
        # plot_consensus_curve(stddevs, iterations)
        if(iter < miniter):
            miniter = iter
            bestEdge = e

        # Remove edge by restoring previous matrix
        graph.remove_edge(e[0], e[1])
        A = B
    print(str(miniter) +" "+ str(bestEdge))


def best_two(graph, A):
    n = graph.number_of_nodes()
    alles = generate_all_edges(n, A)
    print(len(alles))
    alltwos = [(e1, e2) for e1 in alles for e2 in alles if (e1 != e2)]
    miniter = 1001 # pseudo max integer
    bestEdges = ((), ())

    print(len(alltwos))

    for (e1, e2) in alltwos:
        # Save restore point
        B = deepcopy(A)
        add_edge(e1[0], e1[1], A, graph)
        add_edge(e2[0], e2[1], A, graph)

        iter = 0
        for x in range(200):
            values = rand_val(10)
            iter += len(find_consensus(A, values))
        
        iter = iter / float(200)
        #iter = len(stddevs)
        #iterations = [k for k in range(iter)]
        # plot_consensus_curve(stddevs, iterations)
        if(iter < miniter):
            miniter = iter
            bestEdges = (e1, e2)

        # Remove edge by restoring previous matrix
        graph.remove_edge(e1[0], e1[1])
        graph.remove_edge(e2[0], e2[1])
        A = B
    
    print(str(miniter) +" "+ str(bestEdges))

main()