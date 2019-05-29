import networkx as nx
import random
import numpy as np
import tools
## Place graphs here


# 2-star non-random
hossein = nx.Graph()
hossein.add_edges_from([(0,1), (2,1), (1,3), (3,4), (3,5)])
pos = [(0, 0), (333, 500), (0, 1000), (666, 500), (1000, 1000), (1000, 0)]
tools.randomize_pos_and_cost(hossein, pos)
#####


#####
john = nx.Graph()
john.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0), (0, 4), (0, 5), (1, 6), (2, 7), (2, 8), (2, 9), (3, 10), (3, 11), (3, 12), (3, 13)])
pos = [(400,600), (800,600), (800,300), (400,300), (0,1000), (100,1000), (1000,1000), (1000,200), (900,100), (800,0), (0,300), (100,100), (200,0), (400,0)]
tools.randomize_pos_and_cost(john, pos)
#####

#####
# Star-15
star_15 = nx.star_graph(15)
pos = [(500, 500), (0,1000), (250,1000), (500,1000), (750, 1000), (1000,1000), (1000,750), (1000,500), (1000,250), (1000,0), (750,0), (500,0), (250,0), (0,0), (0,250), (0,500)]
tools.randomize_pos_and_cost(star_15, pos)
#####

####
# Star-6
star_6r = nx.star_graph(6)
pos = [(500,500), (100,800), (300,1000), (800,1000), (1000,600), (700,100), (250,200)]
tools.randomize_pos_and_cost(star_6r)
####

####
# Bull
bull = nx.bull_graph()
pos = [(500,0), (200,400), (800,400), (100,700), (900,700)]
tools.randomize_pos_and_cost(bull)
####

####
# Maze
#maze_r = nx.sedgewick_maze_graph()
#tools.randomize_pos_and_cost(maze_r)
####

####
# Maze non-random
maze = nx.sedgewick_maze_graph()
pos = [(333, 750), (1000, 0), (333, 1000), (0, 0), (333, 250), (0, 500), (666, 750), (666, 250)]
tools.randomize_pos_and_cost(maze, pos)

####
# Star-6 non-random
star_6 = nx.star_graph(6)
pos = [(500, 500), (500, 1000), (900, 750), (900, 250), (500, 0), (100, 250), (100, 750)]
tools.randomize_pos_and_cost(star_6, pos)
####
