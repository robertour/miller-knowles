import random
import csv

from sortedcontainers import SortedList, SortedSet, SortedDict

from operator import itemgetter
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from games import PD
from networkx.classes.function import neighbors
from astropy.units import count

class SocialNetwork(object):
    COOP = 'C'
    DEFE = 'D'
    strategies = ['C', 'D']

    def __init__(self, b=1, n_per_gen=10, e_per_gen=2, epsilon=.99, max=1000,
                 tourn=0.01, X=0.025):
        self.b = b
        self.n_per_gen = n_per_gen
        self.e_per_gen = e_per_gen
        self.epsilon = epsilon
        self.max = max
        self.tourn = tourn
        self.X = X
        
        self.gen = 0
        self.count = 0
        self.cooperators = 0
        self.size = 0
        g = self.g = nx.Graph()

        self._max = max+n_per_gen
        self.fitness = np.empty(self._max)
        self.fitness_of = np.empty(self._max, dtype=np.int_)
        self.free_indexes = []
        self.node_set = SortedSet()
        
        for i in range(0, self._max):
            self.fitness_of[i] = -1
            self.free_indexes.append(i)

        self.add_node(self.__class__.COOP, self.gen)
        self.add_node(self.__class__.COOP, self.gen)
        self.add_node(self.__class__.COOP, self.gen)
        
        g.add_edge(0, 1)
        g.add_edge(0, 2)
        g.add_edge(1, 2)
        
        self.game = PD(b, self.fitness)


    def add_node(self, st, gen):
        id = self.count
        r_index = self.free_indexes.pop()
        self.g.add_node(id, st=st, nst=st, r_index=r_index, gen=gen)
        self.node_set.add(id)
        self.fitness_of[r_index] = id
        self.fitness[r_index] = 0
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
                    
                    if random.random() < (1.0 * (r_n2 - r_n1) / \
                         self.b * max(len(neighbors_n1), \
                                      len(g.neighbors(n2_index)))):
                        # update the strategy to a temporary vector
                        n1[1]['nst'] = n2['st']

                    
                    # Poncela´s Formula gives to much weight to the number 
                    # of nodes, this is an alternate version
                    # probability P = neighbour_fitness   focal_node_fitness
                    #                 ------------------ - -----------------
                    #                  b * k_neighbour      b * k_focal_node

                    # if random.random() < (1.0 * r_n2) / \
                    # (self.b*len(g.neighbors(n2_index)))- \
                    # (1.0 * r_n1) / \
                    # (self.b*len(neighbors_n1)):
                    # n1[1]['nst'] = n2['st']
            
            # update coop counter
            if n1[1]['nst'] == self.__class__.COOP:
                cooperators += 1
                
        self.cooperators = cooperators
    
    def growth_initial(self, growth):
        if self.size < self.n_per_gen:
            temp = self.n_per_gen
            self.n_per_gen = self.n_per_gen - self.count
            growth()
            self.n_per_gen = temp

    def growth_cra(self):
        f_of = self.fitness_of
        g = self.g
        node = g.node
        node_set = self.node_set
        
        # temporary holder for fitness values and indexes 
        temp_fitness = []
                
        for i in range(self.n_per_gen):
            
            # add the node to the network
            n_id = self.add_node(random.choice(self.__class__.strategies), 
                                 self.gen)
            
            # select the nodes to be connected with            
            selected = random.sample(node_set,self.e_per_gen)
            
            # connect the node to e_per_gen nodes (edges)
            for node in selected:
          
                # add the edge
                g.add_edge(n_id, node)
                
    
    def growth_epa(self):
        f_of = self.fitness_of
        fitness = self.fitness
        
        # TODO this should innecessary !!!!!!!
        # calculate probabilities
        #survival[f_of != -1] = 1 - self.epsilon + \
        #                       self.epsilon * self.fitness[f_of != -1]
        
        
        #survival /= sum(survival[f_of != -1])
        max_sum = sum(fitness[f_of != -1])
        
                        
        for i in range(self.n_per_gen):
            
            # add the node to the network
            n_id = self.add_node(random.choice(self.__class__.strategies), 
                                 self.gen)
        
            temp_fitness = []
                
            # connect the node to e_per_gen nodes (edges)
            for e in range(self.e_per_gen):
                
                # get the winner fitness index
                r_index = self.choose_r_index(fitness, max_sum)
                                
                # add the edge
                self.g.add_edge(n_id, f_of[r_index])
                
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

    
    def choose_r_index(self, s, max_sum):
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
        for key,value in sorted_fit.items():
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
            if value['nst'] == self.__class__.COOP:
                coop += 1
        return coop
