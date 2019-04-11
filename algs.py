import tools
import math
import random as rn
from itertools import combinations

### Exhaustive: Finding best edge(s) ###

def exhaustive(graph_0, A_0, depth=1, all_edges=None, min_x=math.inf, func=tools.sec_larg_eig):
    # best_graph = graph_0
    # best_edge_s = []
    # best_A = A_0

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


