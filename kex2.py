import numpy as np
import matplotlib.pyplot as plt
import sys
import networkx as nx
from copy import deepcopy
import random
import tools
import graphs
import algs

### Exhaustive search test ###
def exhaustive_test(graph, depth=None, func=tools.sec_larg_eig):
    A = tools.generate_A(graph)
    init_val = func(graph, A)
    eig = 1 # initial eig
    val_list = []

    if depth != None:
        s_largest, best_graph, best_edge, _ = algs.exhaustive(graph, A, depth, func=func)
        print_details(s_largest, best_graph, best_edge)
    else:
        all_edges = tools.generate_all_edges(graph, A)
        n = len(all_edges)
        top_n = 0
        print_details(init_val, graph, None, print_it=False)
        val_list.append(init_val)

        for i in range(1, n + 1):
            val, best_graph, best_edge, _ = algs.exhaustive(graph, A, i, func=func)
            #print(best_edge)
            print_details(val, best_graph, best_edge, print_it=False)
            val_list.append(val)
            
    return np.asarray(val_list)

### Greedy search test ###
def greedy_test(graph, depth=None, func=tools.sec_larg_eig):
    A = tools.generate_A(graph)
    all_edges = tools.generate_all_edges(graph, A)
    init_val = func(graph, A)
    val_list = [init_val]
    
    if depth != None:
        eig, graph, edge_list, A = algs.greedy(graph, A, depth)
        print_details(eig, graph, edge_list, print_it=True)
    else:
        for i in range(1, len(all_edges) + 1):
            val, graph, edge_list, A = algs.greedy(graph, A, func=func)
            #print_details(val, graph, edge_list, print_it=False)
            val_list.append(val)
        
    return np.asarray(val_list)

### Random search test ###
def random_test(graph, depth=None, func=tools.sec_larg_eig):
    A = tools.generate_A(graph)
    all_edges = tools.generate_all_edges(graph, A)
    init_val = func(graph, A)
    val_list = [init_val]
    if depth == None:
        depth = len(all_edges)+1

    for i in range(1, depth):
        val, graph, edge_list, A = algs.random(graph, A, func=func)
        #print_details(val, graph, edge_list, print_it=False)
        val_list.append(val)
    
    return np.asarray(val_list)

### Flow search test ###
def flow_test(graph, depth, func=tools.total_energy):
    A = tools.generate_A(graph)
    val_list = [func(graph, A)]
    if depth == None:
        depth = len(tools.generate_all_edges(graph, A))+1
    for _ in range(1, depth):
        graph, A = algs.flow(graph, A, func=func)
        val = func(graph, A)
        val_list.append(val)
    return np.asarray(val_list)

### Simulated annealing search test ###
def anneal_test(graph_0, depth, func=tools.total_energy):
    A_0 = tools.generate_A(graph_0)
    val_list = [func(graph_0, A_0)]
    addable = tools.generate_all_edges(graph_0, A_0)
    if depth == None:
        depth = len(addable) + 1
    for i in range(1, depth):
        state = algs.anneal(graph_0, A_0, i, func=func)
        graph = state[0]
        A = state[1]
        val = func(graph, A)
        val_list.append(val)
    return np.asarray(val_list)

def tests(amount, graph, depth=None, func=tools.sec_larg_eig):
    exh_result = exhaustive_test(graph, depth, func)
    gre_result = greedy_test(graph, depth, func)
    ran_result = random_test(graph, depth, func)
    flo_result = flow_test(graph, depth, func)
    ann_result = anneal_test(graph, depth, func)

    for i in range(amount):
        # Reinitialize graph
        tools.randomize_pos_and_cost(graph)

        exh_result += exhaustive_test(graph, depth, func)
        gre_result += greedy_test(graph, depth, func)
        ran_result += random_test(graph, depth, func)
        flo_result += flow_test(graph, depth, func)
        ann_result += anneal_test(graph, depth, func)

    exh_result /= amount
    gre_result /= amount
    ran_result /= amount
    flo_result /= amount
    ann_result /= amount

    return exh_result, gre_result, ran_result, flo_result, ann_result

def print_details(value, graph, best_edge=None, print_it=True):
    total_cost = tools.get_total_cost(graph)
    
    print('VALUE: ' + str(value) + '; TOTAL COST: ' + str(total_cost))

    if print_it:
        tools.print_graph(graph, best_edge)


def main():
    graph = getattr(graphs, sys.argv[1])
    depth = int(sys.argv[2]) if len(sys.argv) > 2 else None
    func = tools.total_energy

    #exh_list = exhaustive_test(graph, depth, func=func)  
    #gre_list = greedy_test(graph, depth, func=func)  
    exh_list, gre_list, ran_list, flo_list, ann_list = tests(50, graph, depth, func=func)
    #flo_list = flow_test(graph, depth, func=func)
    x_axis = [i for i in range(len(gre_list))]

    plt.plot(x_axis, exh_list, label="Exhaustive")
    plt.plot(x_axis, gre_list, label="Greedy")
    plt.plot(x_axis, ran_list, label="Random")
    plt.plot(x_axis, flo_list, label="Flow")
    plt.plot(x_axis, ann_list, label="Simulated Annealing")
    plt.title(sys.argv[1])
    plt.legend()
    plt.show()

main()