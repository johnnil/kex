import numpy as np
import matplotlib.pyplot as plt
import sys
import networkx as nx
from copy import deepcopy
import random
import tools
import graphs

def number_of_edges_test(graph, depth=None):
    A = tools.generate_A(graph)
    initial_eig = tools.sec_larg_eig(A)

    if depth != None:
        s_largest, best_graph, best_edge = tools.find_best_edge(graph, A, int(depth), min_eigen=initial_eig)
        print_details(s_largest, best_graph, best_edge)
    else:
        all_edges = tools.generate_all_edges(graph, A)
        n = len(all_edges)
        top_eig = initial_eig
        top_n = 0

        for i in range(1, n + 1):
            new_eig, best_graph, best_edge = tools.find_best_edge(graph, A, i, min_eigen=initial_eig)
            print_details(new_eig, best_graph, print_it=False)
            
            if new_eig < top_eig:
                top_eig = new_eig
                top_n = i
            else:
                print("No graph with " + str(i) + " edges was significantly better than the best with " + str(top_n) + ".")



def print_details(eigenvalue, graph, best_edge=None, print_it=True):
    total_cost = tools.get_total_cost(graph)
    
    print('SECOND LARGEST EIGENVALUE: ' + str(eigenvalue) + '; TOTAL COST: ' + str(total_cost))

    if print_it:
        tools.print_graph(graph, best_edge)


def main():
    graph = getattr(graphs, sys.argv[1])
    depth = sys.argv[2] if len(sys.argv) > 2 else None

    number_of_edges_test(graph, depth)    
    

main()