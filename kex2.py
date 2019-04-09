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
            print_details(val, best_graph, best_edge, print_it=False)
            val_list.append(val)
            
    return val_list

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

def tests(amount, graph, depth=None, func=tools.sec_larg_eig):
    ran_result = random_test(graph, depth, func)
    #gre_result = greedy_test(graph, depth, func)

    for i in range(amount):
        ran_result += random_test(graph, depth, func)
        #gre_result += greedy_test(graph, depth, func)
    
    ran_result /= amount
    #gre_result /= amount
    return ran_result



def print_details(value, graph, best_edge=None, print_it=True):
    total_cost = tools.get_total_cost(graph)
    
    print('VALUE: ' + str(value) + '; TOTAL COST: ' + str(total_cost))

    if print_it:
        tools.print_graph(graph, best_edge)


def main():
    graph = getattr(graphs, sys.argv[1])
    depth = int(sys.argv[2]) if len(sys.argv) > 2 else None
    func = tools.sec_larg_eig

    exh_list = exhaustive_test(graph, depth, func=func)  
    gre_list = greedy_test(graph, depth, func=func)  
    ran_list = tests(1000, graph, depth=None, func=func)
    x_axis = [i for i in range(len(gre_list))]

    plt.plot(x_axis, exh_list, label="exhaustive")
    plt.plot(x_axis, gre_list, label="greedy")
    plt.plot(x_axis, ran_list, label="random")
    plt.title(sys.argv[1])
    plt.legend()
    plt.show()

main()