import tools

### Exhaustive: Finding best edge(s) ###

def exhaustive(graph_0, A_0, depth=1, all_edges=None, min_eigen=1):
    best_graph = graph_0
    best_edge_s = None
    best_A = None

    if (all_edges == None):
        all_edges = tools.generate_all_edges(graph_0, A_0)

    for i, e in enumerate(all_edges):
        # add potential edge
        graph, A = tools.add_edge(e[0], e[1], A_0, graph_0)
        eig_value = tools.sec_larg_eig(A)

        if depth > 1 and i + 1 < len(all_edges):
            eig_value, graph, e2, _ = exhaustive(graph, A, depth - 1, all_edges[i + 1:])
            
            # Started as a debug statement now we here
            if e2 != None:
                e2.append(e)
                e = e2

        if eig_value < min_eigen:
            min_eigen = eig_value
            best_graph = graph
            best_edge_s = e if type(e) == list else [e]
            best_A = A

    return min_eigen, best_graph, best_edge_s, best_A

### Greedy ###

def greedy(graph, A, depth=1):
    edge_list = []
    eig = 0

    for i in range(depth):
        eig, graph, best_edge, A = exhaustive(graph, A)

        if best_edge != None:
            edge_list = edge_list + best_edge
        else:
            # Debug
            print("best edge = None")

    return eig, graph, edge_list

### Heuristics ###

# def random(graph, A, depth=1):
