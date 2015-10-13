import random
import time
import csv
import sys

from sortedcontainers import SortedSet
import networkx as nx
from networkx.classes.function import neighbors
from networkx.classes import graph
from networkx.classes.graph import Graph
import matplotlib.pyplot as plt
import numpy as np
from sortedcontainers.sortedlist import SortedList
np.set_printoptions(threshold=np.nan)

from games import PD

from variables import *

class SocialNetwork(object):
    ID = 0
    
    strategies = [COOP, DEFE]

    def __init__(self, 
                 fluct,
                 rep,
                 nt_seed,
                 nt_desc,
                 nt_randomseed,
                 coop_prob = JUST_COOPERATORS,
                 randomseed = None,
                 b=1,                   
                 n_per_gen=10, 
                 e_per_gen=2, 
                 epsilon = 0.99,
                 max=1000, 
                 tourn=0.01, 
                 X=0.025,
                 K=sys.maxsize,
                 X2= 0.025):

        # this is for identification of the network
        self.id = self.__class__.ID
        self.__class__.ID += 1
        self.fluct = fluct
             
        self.rep = rep
        self.nt_desc = nt_desc
        self.nt_randomseed = nt_randomseed
        self.coop_prob = coop_prob
        
        # set the PD game
        self.T = b
        self.R = 1
        self.P = 0
        self.S = 0               
        
        # seed for the network, this is useful to replicate exactly the same
        # experiment, particularly useful for debugging
        if randomseed == None:
            self.randomseed = time.time()
        else:
            print("WARNING: random seed is not null. Are you sure?")
            self.randomseed = randomseed
        random.seed(self.randomseed)
        
        # main parameters
        self.b = b
        self.n_per_gen = n_per_gen
        self.e_per_gen = e_per_gen
        if (epsilon >= 1.0):
            raise ValueError("""Epsilon cannot be bigger or equal to 1.0.
                             You can use epsilon that are similar to 1.0, 
                             e.g 0.999999999 """)
        else:
            self.epsilon = epsilon
        self.max = max
        self.tourn = tourn
        self.X = X
        self.K = K
        self.X2 = X2
        
        # counters
        self.gen = 0
        self.count = 0
        self.cooperators = 0
        self.removed_nodes = 0
        self.total_fit = 0
        self.total_efit = 0
        self.degrees = 0
        self.size = 0
        g = self.g = nx.Graph()

        # crate auxiliary network structures to increase efficiency
        self._max = max+n_per_gen
        self.eps_fitness = np.empty(self._max)
        self.degrees = np.empty(self._max)
        self.fitness = np.empty(self._max)
        self.fitness_of = np.empty(self._max, dtype=np.int_)
        self.free_indexes = []
        self.node_set = SortedSet()
        
        # initialize the auxiliary structures
        for i in range(0, self._max):
            self.degrees[i] = 0
            self.fitness_of[i] = -1
            self.free_indexes.append(i)
       
        # create the network 
        self.__create_from_seed(nt_seed, coop_prob)
        
        # define the game the nodes are going to play
        self.game = PD(b, self.fitness)
        
        self.treatment = '_'.join(str(x) for x in (self.nt_desc, 
                                                   self.coop_prob,
                                                   self.fluct, self.b, 
                                                   self.X))
        
        self.signature = str(self.id) + '_' + \
                         str(self.rep) + '(' + self.treatment + ')'
        

    def __create_from_seed(self, seed, coop_prob):
        """ This method use the networks structure that comes in the parameter 
        seed as a template for the graph. It adds the necessary attributes to 
        run the algorithm, such as which nodes are cooperators and defectors 
        based on the coop_prob parameter. A value from 0 to 1 indicating a 
        probability of any node of being a cooperators.
        
        Assumes that it is called from the constructor. So it assumes a new 
        SocialNetwork.
        """   
        self.count = -1
        g = self.g
        
        # add nodes from the seed to the network 
        for node in seed.nodes_iter(data = True):
            # define the attributes of the node 
            id = node[0]          
            if coop_prob == 1 or random.uniform(0,1) < coop_prob:
                st = COOP
                self.cooperators += 1
            else:
                st = DEFE
            r_index = self.free_indexes.pop()   
            
            # add the node
            g.add_node(id, st=st, nst=st, r_index=r_index)
            
            self.node_set.add(id)
            self.fitness_of[r_index] = id
            self.fitness[r_index] = 0
            
            # update parameters of the graph
            if id > self.count: 
                self.count = id
            self.size += 1

        self.count += 1
        
        # add edges from the seed to the network
        for e0, e1 in seed.edges_iter():
            g.add_edge(e0, e1)
            
        self.__remove_isolated_nodes()
        
    
    def __remove_isolated_nodes(self):
        g = self.g
        to_remove = []
        for n, adj in g.adj.items():
            if (len(adj) == 0):
                to_remove.append(n)
                
        for n in to_remove:
            r_index = g.node[n]['r_index']
            self.fitness_of[r_index] = -1
            self.free_indexes.append(r_index)
            self.node_set.discard(n)
            g.remove_node(n)
            self.size -= 1
    
    def add_node(self, st):
        """ Add a node to the network
        """
        # calculate rest of the node attributes
        id = self.count
        r_index = self.free_indexes.pop()
        
        # add node
        self.g.add_node(id, st=st, nst=st, r_index=r_index, gen=self.gen)
        
        # update network structures
        self.node_set.add(id)
        self.fitness_of[r_index] = id
        self.fitness[r_index] = 0
        self.degrees[r_index] = 0
        
        # update network parameters
        if st == COOP:
            self.cooperators += 1
        self.size += 1
        self.count += 1
        
        return id


    def play_games_and_remove_isolated_nodes(self):
        g = self.g
        node = g.node
        node_set = self.node_set
        adjacency = self.g.adj
        f = self.fitness
        ef = self.eps_fitness
        eps = self.epsilon
        degrees = self.degrees
                
        f.fill(0)

        total_fit = 0
        total_efit = 0
        total_degrees = 0
        to_remove=[]
        
        for n1 in node_set:
            adj = adjacency[n1]
            len_adj = len(adj)

            # make sure to remove the nodes that has no more edges
            if (len_adj == 0):
                to_remove.append(n1)
                self.removed_nodes += 1
            else:
                att1 = node[n1]
                r_index1 = att1['r_index']    
                
                #update the strategy
                n1_e = att1['st'] = att1['nst']
                                              
                # play against all the neighbors
                for n2 in adj.keys():
                    # make sure to play just once, nodes should be in order
                                    # make sure all the adjacent nodes are in order
                    
                    if (n2 > n1):
                        att2 = node[n2]
                        if n1_e == att2['nst']:
                            if n1_e == COOP:
                                f[r_index1] += self.R
                                f[att2['r_index']] += self.R
                                total_fit += self.R + self.R
                            else:
                                f[r_index1] += self.P
                                f[att2['r_index']] += self.P
                                total_fit += self.P + self.P
                        else:
                            if n1_e == COOP:
                                f[r_index1] += self.S
                                f[att2['r_index']] += self.T
                                total_fit += self.S + self.T
                            else:
                                f[r_index1] += self.T
                                f[att2['r_index']] += self.S
                                total_fit += self.T + self.S
                
                # this epsilon is important to give some of the nodes 
                # some chance to cooperate
                ef[r_index1] = 1 - eps + eps * f[r_index1]
                total_efit += ef[r_index1]
                
                # keep the degrees updates for PA
                degrees[r_index1] = len_adj
                total_degrees += degrees[r_index1]
                
                       
        # set the class attribute
        self.total_fit = total_fit
        self.total_efit = total_efit
        self.total_degrees = total_degrees
        
        # population will  collapse
        if self.size - len(to_remove) < self.e_per_gen:
            print ("population collapsed with", 
                   count_coop(sn), "cooperators and",
                   self.size - count_coop(sn), "defectors" )

        # remove nodes that didn't have any edges            
        for n in to_remove:
            r_index = g.node[n]['r_index']
            self.fitness_of[r_index] = -1
            self.free_indexes.append(r_index)
            self.node_set.discard(n)
            g.remove_node(n)
            self.size -= 1

        
    def update_strategies(self):
        g = self.g
        self.gen += 1
        cooperators = 0
        degrees = self.degrees
        
        for n1 in g.nodes_iter(data = True):
            
            neighbors_n1 = g.neighbors(n1[0])
            r_index1 = n1[1]['r_index']
                        
            n2_index = random.choice(neighbors_n1)
            n2 = g.node[n2_index]
            
            # check that the strategies are actually different
            if n1[1]['st'] != n2['st']:
                
                r_n1 = self.fitness[r_index1]
                r_n2 = self.fitness[n2['r_index']]
                
                # Look to see if difference is less than a millionth of
                # largest value and then assume equivalence
                epsilon_fitness = max(r_n2,r_n1) / 1000000
                
                # if the neighbor has a bigger accumulated fitness
                if r_n2 > r_n1 + epsilon_fitness:
                    
                    #   probP = (neighbour_fitness - focal_node_fitness)
                    #           ----------------------------------------
                    #               b * max[k_focal_node, k_neighbour]
                    
                    if random.random() < \
                            (1.0 * (r_n2 - r_n1)) / \
                            (self.b * max(len(neighbors_n1), \
                            len(g.neighbors(n2_index)))):
                        # update the strategy to a temporary vector
                        n1[1]['nst'] = n2['st']

                    
                    """
                    Poncela´s Formula gives to much weight to the number 
                    of nodes, this is an alternate version that would be
                    worth to test:
                      
                    probability P = neighbour_fitness   focal_node_fitness
                                    ------------------ - -----------------
                                     b * k_neighbour      b * k_focal_node

                    
                    if random.random() < (1.0 * r_n2) / \
                                         (self.b*len(g.neighbors(n2_index)))-\
                                         (1.0 * r_n1) / \
                                         (self.b*len(neighbors_n1)):
                     n1[1]['nst'] = n2['st']
                     """
            
            # update cooperators counter
            if n1[1]['nst'] == COOP:
                cooperators += 1
                
        self.cooperators = cooperators
    
    
    def growth_initial(self, growth):
        """ This method make sure that the first growth completes the nodes
        necessary to get to a consistent increment of 10 per generation. It
        just applies for starting networks that are smaller than self.n_per_gen 
        """
        if self.size < self.n_per_gen:
            temp = self.n_per_gen
            self.n_per_gen = self.n_per_gen - self.count
            growth(self)
            self.n_per_gen = temp



    def attrition(self, selection_method):
        g = self.g

        # it should be call losers
        winners = selection_method(self)
      
        # remove the winning nodes
        for winner in winners:    
            # remove the node from the graph and update fitness arrays
            r_index = g.node[winner]['r_index']
            self.fitness_of[r_index] = -1
            self.free_indexes.append(r_index)
            self.node_set.discard(winner)
            g.remove_node(winner)
            self.size -= 1
            
        # I have moved the removal of nodes with no edges to the play_games 
        # phase to save optimize the code. The auxiliary method remove_isolated
        # has been created in order to produce real results.
        
    def remove_isolated(self, select_winners):
        g = self.g
        to_remove = []

        for n, adj in g.adj.items():
            if (len(adj) == 0):
                to_remove.append(n)
                self.removed_nodes += 1
        
        if self.size - len(to_remove) < self.e_per_gen:
            print ("population collapsed with", 
                   self.count_coop(), "cooperators and",
                   self.size - self.count_coop(), "defectors" )
            
        for n in to_remove:
            r_index = g.node[n]['r_index']
            self.fitness_of[r_index] = -1
            self.free_indexes.append(r_index)
            self.node_set.discard(n)
            g.remove_node(n)
            self.size -= 1