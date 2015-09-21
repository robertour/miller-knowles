import random
import csv


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
        g = self.g = nx.Graph()

        self.fitness = np.empty(max+n_per_gen)
        self.survival = np.empty(max+n_per_gen)
        self.fitness_of = np.empty(max+n_per_gen, dtype=np.int_)
        self.free_indexes = []
        
        for i in range(0, max+n_per_gen):
            self.survival[i] = self.fitness[i] = 0
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
        self.fitness_of[r_index] = id
        self.fitness[r_index] = 0
        self.count += 1
        return id

    def play_games(self):
        g = self.g
        # TODO this is very inneficient
        # look for a better way to do this!!!!!!!
        nodes = dict(g.nodes(data=True))
        r = self.fitness.fill(0)
        
        
        #nx.get_node_attributes(self.g, 0)
        
        #print(nodes)
        #print(self.g.edges())
        #print(self.g.nodes(data =True))
        for e in g.edges_iter():
            self.game.play(nodes[e[0]], nodes[e[1]])
        #print(self.g.nodes(data =True))


    def update_strategies(self):
        g = self.g
                
        self.gen += 1

        for n1 in g.nodes_iter(data = True):
            
            neighbors_n1 = g.neighbors(n1[0])
            if len(neighbors_n1) == 0:
                print("an isolated neighbor")
            else:
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
                            # TODO this is incorrect but might be affecting the results
                            n1[1]['nst'] = n1[1]['st'] = n2['st']
    
                        #probability P =   neighbour_fitness     focal_node_fitness
                        #                  ------------------ - --------------------
                        #                    b * k_neighbour      b * k_focal_node
    
    #                     if random.random() < (1.0 * r_n2) / \
    #                                          (self.b*len(g.neighbors(n2_index)))- \
    #                                          (1.0 * r_n1) / \
    #                                          (self.b*len(neighbors_n1)):
    #                         n1[1]['nst'] = n2['st']
        
    
    def growth_initial(self):
        if self.count < self.n_per_gen:
            temp = self.n_per_gen
            self.n_per_gen = self.n_per_gen - self.count
            self.growth()
            self.n_per_gen = temp
    
    def growth(self,):
        f_of = self.fitness_of
        survival = self.survival
        
        # calculate probabilities
        survival[f_of != -1] = 1 - self.epsilon + \
                               self.epsilon * self.fitness[f_of != -1] * 1.0
        
        survival /= sum(survival[f_of != -1])
        
        # temporary holder for fitness values and indexes 
        temp_fitness = []
                
        for i in range(self.n_per_gen):
            
            # add the node to the network
            n_id = self.add_node(random.choice(self.__class__.strategies), 
                                 self.gen)
            
            # connect the node to e_per_gen nodes (edges)
            for e in range(self.e_per_gen):
                
                # get the winner fitness index
                r_index = self.choose_r_index()
                
                # add the edge
                self.g.add_edge(n_id, f_of[r_index])
                
                # temporarily store the r index and fitness values
                temp_fitness.append((r_index, survival[r_index]))
                
                # temporarily reduce probability to 0, so it won't be chosen
                # again
                survival[r_index] = 0

            # restore the fitness array after adding the edges
            for r_index, val in temp_fitness:
                survival[r_index] = val

    def choose_r_index(self):
        s = self.survival
        max = sum(s)
        picked_value = random.uniform(0, max)
        
        current_value = 0
        for index in range(0,len(s)):
            current_value += s[index]
            if current_value > picked_value:
                return index
        
        return len(s) - 1

    def attrition(self):
        
        g = self.g
                
        size = len(g)

        # in Steve's code he uses int instead of round
        # TODO put back to round
        for i in range(0,int(size*self.X)):       
            
            # #TODO avoid repetitions randomly select the participants
           #  tombola = random.sample(g.nodes(data=True), round(size*self.tourn))
            
            
            #following millers approach
            tombola = [] 
            for i in range(10):
                tombola.append(random.choice(g.nodes(data=True)))
            
            
            # search for the "winners" (or really "losers")
            min_fit = float("inf")
            ties = []
            for t in tombola:
                cur_fit = self.fitness[t[1]['r_index']]
                if cur_fit < min_fit:
                    min_fit = cur_fit
                    ties=[t]
                elif cur_fit == min_fit:
                    ties.append(t)

            # in case of tie, select one randomly
            winner = random.choice(ties)
            
            # remove the node from the graph and update fitness arrays
            r_index = winner[1]['r_index']
            self.fitness_of[r_index] = -1
            self.survival[r_index] = 0
            self.free_indexes.append(r_index)
            g.remove_node(winner[0])

            
        components = list(nx.connected_component_subgraphs(g))
  
        # Remove isolated nodes
        for i in range(0, len(components)):
            if len(components[i]) == 1:
                for n in components[i].nodes(data = True):
                    r_index = n[1]['r_index']
                    self.fitness_of[r_index] = -1
                    # important to clean because it is not reinitialized as fitness
                    self.survival[r_index] = 0
                    self.free_indexes.append(r_index)
                    g.remove_node(n[0])

        #REMOVE ALL ISOLATED SUBGRAPHS
#         for i in range(1, len(components)):
#             for n in components[i].nodes(data = True):
#                 r_index = n[1]['r_index']
#                 self.fitness_of[r_index] = -1
#                 # important to clean because it is not reinitialized as fitness
#                 self.survival[r_index] = 0
#                 self.free_indexes.append(r_index)
#                 
#         self.g = components[0]

    def print_results(self, id, treatment, b):
        coop = 0 
        defect = 0
        for i in self.g.nodes(data=True):
            if i[1]['nst'] == self.__class__.COOP:
                coop += 1
            else:
                defect += 1
        print(id,",",treatment,",",b,",",coop,",",defect,",",len(self.g))

    def draw_random(self):
        nx.draw(self.g)
        plt.show()
        
    def draw(self):
        G=self.g
        # find node with largest degree
        node_and_degree=G.degree()
        (largest_hub,degree)=sorted(node_and_degree.items(),key=itemgetter(1))[-1]
        # Create ego graph of main hub
        hub_ego=nx.ego_graph(G,largest_hub)
        # Draw graph
        pos=nx.spring_layout(hub_ego)
        nx.draw(hub_ego,pos,node_color='b',node_size=50,with_labels=False)
        # Draw ego as large and red
        nx.draw_networkx_nodes(hub_ego,pos,nodelist=[largest_hub],node_size=300,node_color='r')
        plt.savefig('ego_graph.png')
        plt.show()