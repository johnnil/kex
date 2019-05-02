import tools
import math
import random as rn
import numpy
from itertools import combinations
from copy import deepcopy

### Exhaustive: Finding best edge(s) ###

def exhaustive(graph_0, A_0, depth=1, all_edges=None, min_x=math.inf, func=tools.sec_larg_eig):
    if (all_edges == None):
        all_edges = tools.generate_all_edges(graph_0, A_0)
    
    combs = combinations(all_edges, depth)

    for i in list(combs):
        graph = graph_0
        A = A_0

        for e in i:
            graph, A = tools.add_edge(e[0], e[1], A, graph)
        
        x = func(graph, A)

        # Better or worse?
        if x < min_x:
            min_x = x
            best_graph = graph
            best_edge_s = i
            best_A = A

    return min_x, best_graph, list(best_edge_s), best_A

### Greedy ###

def greedy(graph, A, depth=1, func=tools.sec_larg_eig):
    edge_list = []

    for i in range(depth):
        eig, graph, best_edge, A = exhaustive(graph, A, func=func)

        if best_edge != None:
            edge_list = edge_list + best_edge
        else:
            # Debug
            print("best edge = None")

    return eig, graph, edge_list, A

### Heuristics ###
## Random ##
def random(graph, A, depth=1, func=tools.sec_larg_eig):
    edge_list = []
    #all possible edges and put them in a magician's hat
    edge_hat = tools.generate_all_edges(graph, A)

    for i in range(depth):
        #add a non-existing edge at random
        edge = edge_hat.pop(rn.randint(0, len(edge_hat)-1))
        edge_list.append(edge)
        graph, A = tools.add_edge(edge[0], edge[1], A, graph)
    
    val = func(graph, A)

    return val, graph, edge_list, A

## Biggest to smallest (largest flow) ##
def flow(graph, A, func=tools.total_energy):
    # nodes with least and most neighbours
    all_edges = tools.generate_all_edges(graph, A)
    max_dist = 0
    n1 = 0
    n2 = 0
    for i in all_edges:
        distance = tools.calc_diff(i[0], i[1], graph)
        if (max_dist < distance):
            max_dist = distance
            n1 = i[0]
            n2 = i[1]
    
    newGraph, newA = tools.add_edge(n1, n2, A, graph)
    return newGraph, newA
    
## Simulated Annealing ##
# Returns a neighbouring state
def neighbour(graph, A_0, removable_0, addable_0):
    removable = deepcopy(removable_0)
    addable = deepcopy(addable_0)
    # Swap a non-base edge with an addable at random
    old = removable.pop(rn.randint(0,len(removable)-1))
    new = addable.pop(rn.randint(0,len(addable)-1))
    addable.append(old)
    removable.append(new)
    graph, A = tools.remove_edge(old[0], old[1], A_0, graph)
    graph, A = tools.add_edge(new[0], new[1], A, graph)
    #print("Removable in neighb: "+str(removable))
    
    return [graph, A, removable, addable]

def prob(e1, e2, T):
    val = 0
    if(e2 < e1):
        val = 1
    else:
        val = math.exp(-(e2 - e1)/T)
    return val

def anneal(graph_0, A, k, func=tools.total_energy):
    graph = deepcopy(graph_0)
    addable = tools.generate_all_edges(graph, A)

    removable = []
    for _ in range(k):
        # Add an edge to the graph at random
        edge = addable.pop(rn.randint(0, len(addable)-1))
        removable.append(edge)
        graph, A = tools.add_edge(edge[0], edge[1], A, graph)

    #state
    T = 1.0
    Tmin = 0.0001
    alpha = 0.9
    s = [graph, A, removable, addable]
    if (len(addable) == 0):
        return s
    while (T > Tmin):
        # Multiple samples
        for _ in range(10):
            snew = neighbour(s[0],s[1],s[2],s[3])

            if (prob(func(s[0], s[1]), func(snew[0], snew[1]), T) >= numpy.random.random_sample()):
                s = snew

            T = T*alpha
    return s