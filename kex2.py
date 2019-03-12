import numpy as np
import matplotlib.pyplot as plt
import sys
import networkx as nx

hossein = nx.Graph()
hossein.add_edges_from([(0,1), (2,1), (1,3), (3,4), (3,5)])
# A = generateA(hossein)

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
    result = [stddev]
    iter = 0

    while (stddev > 0.01):
        values = update_values(A, values)
        stddev = np.std(values)
        iter += 1
        result.append(stddev)
    
    print(values)
    print(iter)
    return result


def update_values(A, values):
    return np.matmul(A, values)

def plot_consensus_curve(result, iter):
    plt.plot(result, iter)
    plt.show()

def main_helper(graph, A):
    values = [i for i in range(6)]
    result = find_consensus(A, values)
    iterations = [i for i in range(len(result))]
    plot_consensus_curve(iterations, result)

def main():
    A = generateA(hossein)
    main_helper(hossein, A)
    add_edge(4, 5, A, hossein)
    main_helper(hossein, A)

main()