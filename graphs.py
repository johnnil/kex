import networkx as nx
import random
import numpy as np
import tools
## Place graphs here

#####
hossein = nx.Graph()
hossein.add_edges_from([(0,1), (2,1), (1,3), (3,4), (3,5)])
tools.randomize_pos_and_cost(hossein)
#####


#####
john = nx.Graph()
john.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0), (0, 4), (0, 5), (1, 6), (2, 7), (2, 8), (2, 9), (3, 10), (3, 11), (3, 12), (3, 13)])
tools.randomize_pos_and_cost(john)
#####

#####
star = nx.star_graph(15)
tools.randomize_pos_and_cost(star)
#####

