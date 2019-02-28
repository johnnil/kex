# Program for testing consensus reach in different topologies
# Created by John and Jonatan

import igraph

# >-<
g1 = igraph.Graph()
g1.add_vertices(6)
g1.add_edges([(0,1), (2,1), (1,3), (3,4), (3,5)])
g1.vs["value"] = [3, 3, 2, 2, 1, 1]

# Error margin
err = 0.15

def consensus(g, target):
    consensus = True
    for v in g.vs:
        #print(dir(v))
        newAvg = v["value"]
        items = 1
        for n in v.neighbors():
            newAvg += n["value"]
            items += 1
        newAvg = newAvg/float(items)
        if not ((newAvg > target-err) and (newAvg < target+err)):
            consensus = False
        v["value"] = newAvg
        print(consensus)
    return consensus

def printGraph(g):
    for v in g1.vs:
        print("Node: "+str(v.index)+ " value: "+str(v["value"]))
        
def reachConsensus(g):
    # Total number of required iterations through the whole graph
    rounds = 0
    avg = sum(g.vs["value"]) / float(len(g.vs))
    done = False
    while not done:
        done = consensus(g, avg)
        print(done)
        rounds += 1
        printGraph(g)
    print(rounds)

reachConsensus(g1)

g1.write_svg("kexplot", labels='value')