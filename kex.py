# Program for testing consensus reach in different topologies
# Created by John

import igraph

# >-<
g1 = igraph.Graph()
g1.add_vertices(6)
g1.add_edges([(0,1), (2,1), (1,3), (3,4), (3,5)])
g1.vs["value"] = [3, 3, 2, 2, 1, 1]

# _
# H
# -
g2 = igraph.Graph()
g2.add_vertices(6)
g2.add_edges([(0,1), (1,2), (2,3), (3,4), (4,5), (5,0), (2,5)])
g2.vs["value"] = [3, 3, 2, 2, 1, 1]

# Error marging
err = 0.3

def consensus(g, target):
    consensus = True
    for v in g.vs:
        newAvg = v["value"]
        items = 1
        for n in v.neighbors():
            newAvg += n["value"]
            items += 1
        newAvg = newAvg/float(items)
        if not ((newAvg > target-err) and (newAvg < target+err)):
            consensus = False
        v["value"] = newAvg
    return consensus

def printGraph(g):
    for v in g.vs:
        print("Node: "+str(v.index)+ " value: "+str(v["value"]))
        
def reachConsensus(g):
    # Total number of required iterations through the whole graph
    rounds = 0
    avg = sum(g.vs["value"]) / float(len(g.vs))
    done = False
    while not done:
        done = consensus(g, avg)
        # Debugging
        #printGraph(g)
        rounds += 1
    print("\nNumber of rounds: "+str(rounds))
    printGraph(g)

reachConsensus(g1)
reachConsensus(g2)

g1.write_svg("kexplot", labels='value')
g2.write_svg("kexplot2", labels='value')