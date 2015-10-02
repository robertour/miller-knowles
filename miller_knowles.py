import random
import time
import csv

from sortedcontainers import SortedSet, SortedDict

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
np.set_printoptions(threshold=np.nan)

from games import PD
from networkx.classes.function import neighbors
from astropy.units import count
from networkx.classes import graph
from networkx.classes.graph import Graph

from variables import *

class SocialNetwork(object):
    ID = 0
    
    strategies = [COOP, DEFE]

    def __init__(self, 
                 network_seed,
                 network_seed_desc,
                 network_randomseed,
                 coop_prob = JUST_COOPERATORS,
                 randomseed = None,
                 b=1,                   
                 n_per_gen=10, 
                 e_per_gen=2, 
                 max=1000, 
                 tourn=0.01, 
                 X=0.025):

        # this is for identification of the network
        self.id = self.__class__.ID
        self.__class__.ID += 1     
        self.network_seed_desc = network_seed_desc
        self.network_randomseed = network_randomseed  
        self.coop_prob = coop_prob               
        
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
        self.max = max
        self.tourn = tourn
        self.X = X
        
        # counters
        self.gen = 0
        self.count = 0
        self.cooperators = 0
        self.removed_nodes = 0
        self.size = 0
        g = self.g = nx.Graph()

        # crate auxiliary network structures to increase efficiency
        self._max = max+n_per_gen
        self.fitness = np.empty(self._max)
        self.fitness_of = np.empty(self._max, dtype=np.int_)
        self.free_indexes = []
        self.node_set = SortedSet()
        
        # initialize the auxiliary structures
        for i in range(0, self._max):
            self.fitness_of[i] = -1
            self.free_indexes.append(i)
       
        # create the network 
        self.__create_from_seed(network_seed, coop_prob)
        
        # define the game the nodes are going to play
        self.game = PD(b, self.fitness)


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
        
        # update network parameters
        if st == COOP:
            self.cooperators += 1
        self.size += 1
        self.count += 1
        
        return id


    def play_games(self):
        g = self.g
        nodes = g.node
        # TODO if restarted with -1 I could avoid the loop over the edges
        r = self.fitness.fill(0)
        
        for e in g.edges_iter():
            self.game.play(nodes[e[0]], nodes[e[1]])


    def update_strategies(self):
        g = self.g
        self.gen += 1
        cooperators = 0
        
        for n1 in g.nodes_iter(data = True):
            
            neighbors_n1 = g.neighbors(n1[0])
            n2_index = random.choice(neighbors_n1)
            n2 = g.node[n2_index]
            
            # check that the strategies are actually different
            if n1[1]['st'] != n2['st']:
                
                r_n1 = self.fitness[n1[1]['r_index']]
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
            growth()
            self.n_per_gen = temp


    def growth_cra(self):
        g = self.g
        node_set = self.node_set
        e_per_gen = self.e_per_gen
        
        # this are the existent nodes before the growth process
        # miller's nodes doesn't attach to new nodes, that hasn't
        # play yet
        range_of_existent_nodes = range(len(node_set))        
         
                
        for i in range(self.n_per_gen):
            
            # add the node to the network
            n_id = self.add_node(random.choice(self.__class__.strategies))
            
            # select the nodes to be connected with            
            selected = random.sample(range_of_existent_nodes,e_per_gen)
            
            # connect the node to e_per_gen nodes (edges)
            for node_index in selected:
          
                # add the edge
                g.add_edge(n_id, node_set[node_index])
                
    
    def growth_epa(self):
        f_of = self.fitness_of
        fitness = self.fitness
        
        """
        Poncela et. al suggested to use an epsilon of 0.99. No reason is 
        given, but we assumed it is to avoid divisions by 0. However, this 
        is an unnecessary expensive calculation. We avoid this by using the
        __choice_r_index
        survival[f_of != -1] = 1 - 0.99 + \
                              0.99 * self.fitness[f_of != -1]     
        survival /= sum(survival[f_of != -1])
        """
        g = self.g
        n_per_gen = self.n_per_gen
        e_per_gen = self.e_per_gen
        
        elegible_nodes = SortedSet()
        counter_elegible = 0
        max_sum = 0
        for i in range(self._max):
            if f_of[i] != -1:
                if fitness[i] > 0:
                    max_sum += fitness[i]
                    counter_elegible += 1
                    if counter_elegible <= e_per_gen:
                        elegible_nodes.add(f_of[i])
        #max_sum = sum(fitness[f_of != -1])
        
        if counter_elegible > n_per_gen:         
                        
            for i in range(n_per_gen):
                
                # add the node to the network
                n_id = self.add_node(random.choice(self.__class__.strategies))
            
                temp_fitness = []
                    
                # connect the node to e_per_gen nodes (edges)
                for e in range(e_per_gen):
                    
                    # get the winner fitness index
                    r_index = self.__choose_r_index(fitness, max_sum)
                                    
                    # add the edge
                    g.add_edge(n_id, f_of[r_index])
                    
                    # temporarily store the r index and fitness values
                    temp_fitness.append((r_index, fitness[r_index]))
                                    
                    # temporarily reduce probability to 0, so it won't be chosen
                    # again, also substract from the sum of fake probabilities
                    max_sum -= fitness[r_index]
                    fitness[r_index] = 0                
    
                # restore the fitness array after adding the edges
                for r_index, val in temp_fitness:
                    fitness[r_index] = val
                    max_sum += val
        
                # if there is no nodes with reward
        elif counter_elegible == 0:
            self.growth_cra()
        
        elif counter_elegible < n_per_gen:
            node_set = self.node_set
            
            missing = e_per_gen - counter_elegible
            
            for i in range(n_per_gen):
                
                # add the node to the network
                n_id = self.add_node(random.choice(self.__class__.strategies))
                
                # connect the node to e_per_gen nodes (edges)
                for node_index in elegible_nodes:
              
                    # add the edge
                    g.add_edge(n_id, node_index)
            
                temp_fitness = []   
                
                # connect the node to e_per_gen nodes (edges)
                for e in range(missing):
                    
                    # get the winner fitness index
                    r_index = self.__choose_r_index(fitness, max_sum)
                                    
                    # add the edge
                    g.add_edge(n_id, f_of[r_index])
                    
                    # temporarily store the r index and fitness values
                    temp_fitness.append((r_index, fitness[r_index]))
                                    
                    # temporarily reduce probability to 0, so it won't be chosen
                    # again, also substract from the sum of fake probabilities
                    max_sum -= fitness[r_index]
                    fitness[r_index] = 0                
    
                # restore the fitness array after adding the edges
                for r_index, val in temp_fitness:
                    fitness[r_index] = val
                    max_sum += val
        
        elif counter_elegible == n_per_gen:
            node_set = self.node_set
            
            for i in range(n_per_gen):
            
                # add the node to the network
                n_id = self.add_node(random.choice(self.__class__.strategies))
                
                # connect the node to e_per_gen nodes (edges)
                for node_index in elegible_nodes:
              
                    # add the edge
                    g.add_edge(n_id, node_index)
            

    def __choose_r_index(self, s, max_sum):
        if (max_sum == 0):
            return self.g.node[random.choice(self.node_set)]['r_index']
        else:
            picked_value = random.uniform(0, max_sum)
            
            current_value = 0
            for index in range(len(s)):
                current_value += s[index]
                if current_value > picked_value:
                    return index
            
            return len(s) - 1


    def attrition(self, select_winners):
        g = self.g

        winners = select_winners()
        
        for winner in winners:    
            # remove the node from the graph and update fitness arrays
            r_index = g.node[winner]['r_index']
            self.fitness_of[r_index] = -1
            self.free_indexes.append(r_index)
            self.node_set.discard(winner)
            g.remove_node(winner)
            self.size -= 1
        
        to_remove = []

        for n, adj in g.adj.items():
            if (len(adj) == 0):
                to_remove.append(n)
                self.removed_nodes += 1
        
        for n in to_remove:
            r_index = g.node[n]['r_index']
            self.fitness_of[r_index] = -1
            self.free_indexes.append(r_index)
            self.node_set.discard(n)
            g.remove_node(n)
            self.size -= 1

    def tornament_least_fit(self):  
        f_of = self.fitness_of
        f = self.fitness
        node_set = self.node_set
        g = self.g
        
        winners = []
        for i in range(round(self.size*self.X)):

            # avoid repetitions randomly select the participants
            tombola = random.sample(node_set,round(self.size*self.tourn))

            # search for the "winners" (or really "losers")
            min_fit = float("inf")
            ties = []
            for t in tombola:
                cur_fit = f[g.node[t]['r_index']]
                if cur_fit < min_fit:
                    min_fit = cur_fit
                    ties=[t]
                elif cur_fit == min_fit:
                    ties.append(t)
    
            # in case of tie, select one randomly
            w = random.choice(ties)
            winners.append(w)
            # we already know this node won't exist,
            # so we can remove it forever
            f_of[g.node[w]['r_index']] = -1
            node_set.discard(w)

        return winners
    
    def tornament_fittest(self):
        f_of = self.fitness_of
        f = self.fitness
        node_set = self.node_set
        g = self.g
        
        winners = []
        for i in range(round(self.size*self.X)):

            # avoid repetitions randomly select the participants
            tombola = random.sample(node_set,round(self.size*self.tourn))

            # search for the "winners" (or really "losers")
            max_fit = -1
            ties = []
            for t in tombola:
                cur_fit = f[g.node[t]['r_index']]
                if cur_fit > max_fit:
                    max_fit = cur_fit
                    ties=[t]
                elif cur_fit == max_fit:
                    ties.append(t)
    
            # in case of tie, select one randomly
            w = random.choice(ties)
            winners.append(w)
            # we already know this node won't exist,
            # so we can remove it forever
            f_of[g.node[w]['r_index']] = -1
            node_set.discard(w)

        return winners


    def at_random(self):
        return random.sample(self.node_set,round(self.size*self.X))


    def least_fit(self):  
        f_of = self.fitness_of
        f = self.fitness
        node_set = self.node_set
        g = self.g
        
        sorted_fit = SortedDict()
        for i in range(self._max):
            if f_of[i] != -1:
                if f[i] in sorted_fit:
                    sorted_fit[f[i]].append(f_of[i])
                else:
                    sorted_fit[f[i]] = [f_of[i]]
    
        shrink_size = round(self.size*self.X)
        winners = []
        for key in iter(sorted_fit):
            value = sorted_fit[key]
            if len(value) + len(winners) < shrink_size:
                winners.extend(value) 
            elif len(value) + len(winners) == shrink_size:
                winners.extend(value)
                break
            else:
                for v in value:
                    winners.append(v)
                    if len(winners) == shrink_size:
                        break
                break
        
        return winners


    def fittest(self):  
        f_of = self.fitness_of
        f = self.fitness
        node_set = self.node_set
        g = self.g
        
        sorted_fit = SortedDict()
        for i in range(self._max):
            if f_of[i] != -1:
                if f[i] in sorted_fit:
                    sorted_fit[f[i]].append(f_of[i])
                else:
                    sorted_fit[f[i]] = [f_of[i]]
    
        shrink_size = round(self.size*self.X)
        winners = []
        for key in reversed(sorted_fit):
            value = sorted_fit[key]
            if len(value) + len(winners) < shrink_size:
                winners.extend(value) 
            elif len(value) + len(winners) == shrink_size:
                winners.extend(value)
                break
            else:
                for v in value:
                    winners.append(v)
                    if len(winners) == shrink_size:
                        break
                break
            
        return winners



    def count_coop(self):
        coop = 0 
        for key, value in self.g.node.items():
            if value['nst'] == COOP:
                coop += 1
        return coop