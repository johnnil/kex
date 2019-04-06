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
def exhaustive_test(graph, depth=None):
    A = tools.generate_A(graph)
    top_eig = tools.sec_larg_eig(A)
    eig = 1 # initial eig
    eig_list = []

    if depth != None:
        s_largest, best_graph, best_edge, _ = algs.exhaustive(graph, A, depth, min_eigen=eig)
        print_details(s_largest, best_graph, best_edge)
    else:
        all_edges = tools.generate_all_edges(graph, A)
        n = len(all_edges)
        top_n = 0
        print_details(top_eig, graph, None, print_it=False)
        eig_list.append(top_eig)

        for i in range(1, n + 1):
            eig, best_graph, best_edge, _ = algs.exhaustive(graph, A, i, min_eigen=1)
            print_details(eig, best_graph, best_edge, print_it=False)
            eig_list.append(eig)
            
            if eig < top_eig:
                top_eig = eig
                top_n = i
            else:
                print("No graph with " + str(i) + " added edge(s) (" + str(best_graph.number_of_edges() + i) + " edges total) was significantly better than the best with " + str(top_n) + ".")
        
        return eig_list 

### Greedy search test ###
def greedy_test(graph, depth=None):
    A = tools.generate_A(graph)
    all_edges = tools.generate_all_edges(graph, A)
    init_eig = tools.sec_larg_eig(A)
    eig_list = [init_eig]
    
    if depth != None:
        eig, graph, edge_list = algs.greedy(graph, A, depth)
        print_details(eig, graph, edge_list, print_it=True)
    else:
        for i in range(1, len(all_edges) + 1):
            eig, new_graph, edge_list = algs.greedy(graph, A, i)
            print_details(eig, new_graph, edge_list, print_it=False)
            eig_list.append(eig)
        
        return eig_list





def print_details(eigenvalue, graph, best_edge=None, print_it=True):
    total_cost = tools.get_total_cost(graph)
    
    print('LAMBDA2: ' + str(eigenvalue) + '; TOTAL COST: ' + str(total_cost))

    if print_it:
        tools.print_graph(graph, best_edge)


def main():
    graph = getattr(graphs, sys.argv[1])
    depth = int(sys.argv[2]) if len(sys.argv) > 2 else None

    # exh_list = exhaustive_test(graph, depth)    
    gre_list = greedy_test(graph, depth)
    x_axis = [i for i in range(len(gre_list))]

    #plt.plot(x_axis, exh_list, label="exhaustive")
    plt.plot(x_axis, gre_list, label="greedy")
    plt.title(sys.argv[1])
    plt.legend()
    plt.show()

main()