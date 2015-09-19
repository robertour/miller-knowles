import random
import csv

import networkx as nx
import matplotlib.pyplot as plt

class SocialNetwork(object):
    COOP = 'C'
    DEFE = 'D'
    strategies = ['C', 'D']

    def __init__(self):
        self.gen = 0
        self.count = 0
        self.g = nx.Graph()

        self.g.add_node(self.count,
                        strategy=self.__class__.COOP,
                        fitness=0.0,
                        gen=self.gen)
        self.count += 1
        self.g.add_node(self.count,
                        strategy=self.__class__.COOP,
                        fitness=0,
                        atta_p=0.0,
                        gen=self.gen)
        self.count += 1
        self.g.add_node(self.count,
                        strategy=self.__class__.COOP,
                        fitness=0,
                        atta_p=0.0,
                        gen=self.gen)

        self.g.add_edge(0, 1)
        self.g.add_edge(0, 2)
        self.g.add_edge(1, 2)

    def play_pd(self):
        import ipdb; ipdb.set_trace()
        for n in self.g.nodes(data=True):
            print(n)

    def growth(self, nodes):
        if nodes > 1:
            self.gen += 1
            for i in range(nodes):
                self.g.\
                    add_node(self.count,
                            strategy=random.choice(self.__class__.strategies),
                            fitness=0, atta_p=0.0,
                            gen=self.gen)

                self.count += 1

    def draw_random(self):
        nx.draw(self.g)
        plt.show()


sn = SocialNetwork()
#sn.draw_random()
sn.play_pd()
