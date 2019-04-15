import tools
import math
import random as rn

### Exhaustive: Finding best edge(s) ###

def exhaustive(graph_0, A_0, depth=1, all_edges=None, min_x=math.inf, func=tools.sec_larg_eig):
    best_graph = graph_0
    best_edge_s = None
    best_A = A_0

    if (all_edges == None):
        all_edges = tools.generate_all_edges(graph_0, A_0)

    for i, e in enumerate(all_edges):
        # add potential edge
        graph, A = tools.add_edge(e[0], e[1], A_0, graph_0)
        x = func(graph, A)

        if depth > 1 and i + 1 < len(all_edges):
            x, graph, e2, A = exhaustive(graph, A, depth - 1, all_edges[i + 1:], func=func)
            
            # Started as a debug statement now we here
            if e2 != None:
                e2.append(e)
                e = e2

        # Better or worse?
        if x < min_x:
            min_x = x
            best_graph = graph
            best_edge_s = e if type(e) == list else [e]
            best_A = A

    if best_edge_s == None:
        print("here")

    return min_x, best_graph, best_edge_s, best_A

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
    