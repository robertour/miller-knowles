import json
import os
import time
import timeit
import csv
import random
import networkx as nx

from variables import *

from miller_knowles import *
from networkx_to_gephi import n2g
from networkx.generators.random_graphs import gnm_random_graph

class ExperimentController():
    
    def __init__(self, 
                 REP = 10, 
                 GEN = 2000, 
                 SAMPLE = 20,
                 GEPHI = False,
                 network_seeds = [TRIAD],
                 coop_probs=[JUST_COOPERATORS], 
                 growths = ["cra","epa"],
                 attritions = [False, True],
                 selections = [TOURN_LEAST_FIT], 
                 b_s = [1.0,1.3,1.6,1.9,2.2,2.5,2.8],
                 max = 1000,
                 X = [0.025]):
        
        
        self.GEN = GEN
        self.REP = REP
        self.SAMPLE = SAMPLE
        self.GEPHI = GEPHI
        
        self.coop_probs = coop_probs
        self.growths = growths
        self.attritions = []
        self.selections = selections
        
        # it has to be copied like this if not I get ([False, True],)
        for att in attritions:
            self.attritions.append(att)
        self.b_s = b_s
        self.max = max
        self.X = X
    
        self.seeds = []
        for rep in range(self.REP):        
            for desc in network_seeds:
                st = time.time()
                
                if desc == RANDOM_REGULAR_GRAPH:
                    network_seed = nx.random_regular_graph(2,max,seed=st)
                elif desc == ERDOS_RENYI:
                    #network_seed = nx.fast_gnp_random_graph(max,1.0/100,seed=st)
                    # == network_seed = nx.erdos_renyi_graph(1000,0.001,seed=st)
                    network_seed = gnm_random_graph(max,2*max,seed=st)
                elif desc == BARABASI_ALBERT:
                    network_seed = nx.barabasi_albert_graph(max,2,seed=st)
                elif desc == WATTS_STROGATZ:
                    # according to wikipedia N >> K >> ln(1000) >> 0.001
                    # network_seed = 
                    # nx.newman_watts_strogatz_graph(1000, 14, 0.001,seed=st)
                    # 7000 edges
                    network_seed = nx.watts_strogatz_graph(max, 14, 0.01,seed=st) 
                elif desc == TRIAD:
                    network_seed = nx.random_regular_graph(2,3,seed=st)
                else:
                    raise ValueError('Not recognized seed')

                # add the seed to the seeds list                
                self.seeds.append ((rep,{'network_seed': network_seed,
                                         'network_seed_desc' : desc,
                                         'network_randomseed' : st}))

        
        self.timedir = os.path.join("results",time.strftime("%Y%m%d-%H%M%S"))
        if not os.path.exists(self.timedir):
            os.makedirs(self.timedir)


    def run_experiment(self, sn_args_base):
        filename = os.path.join(self.timedir,'fin.csv')
        fp = open(filename, 'w', newline='')
        csvw = csv.writer(fp, delimiter=',')
        csvw.writerow(('id','rep','network',
                       'coop_prob','alg','b','X', 
                       'removed_nodes', 'gen',
                       'cooperators','size','ave','real_time',
                       'network_randomseed', 'randomseed'))
        fp.flush()

        for b in self.b_s:
            for seed in self.seeds:
                sn_args = sn_args_base.copy()
                sn_args.update(seed[1])
                for cp in self.coop_probs:
                    for g in self.growths:
                        for att in self.attritions:
                            if att == '+':
                                runner = self.run_with_attrition
                                for x in self.X:
                                    for s in self.selections:
                                        sn = SocialNetwork(b=b,  
                                                           max=self.max,
                                                           X=x,
                                                           coop_prob = cp,
                                                           **sn_args)
                                        
                                        if s == TOURN_LEAST_FIT:
                                            selection = sn.tornament_least_fit
                                        elif s == TOURN_FITTEST:
                                            selection = sn.tornament_fittest
                                        elif s == LEAST_FIT:
                                            selection = sn.least_fit
                                        elif s == FITTEST:
                                            selection = sn.fittest
                                        else:
                                            selection = sn.at_random
                                                              
                                        if g == "cra":
                                            growth = sn.growth_cra
                                        else:
                                            growth = sn.growth_epa
                                        
                                        self.start(sn=sn, 
                                                   rep=seed[0], 
                                                   alg=g + att + "("+s+")", 
                                                   growth_method=growth, 
                                                   runner=runner, 
                                                   selection_method=selection,
                                                   csv_writer=csvw) 
                            else:
                                runner = self.run_without_attrition
                                
                                sn = SocialNetwork(b=b, 
                                                   X=0,
                                                   max=self.max,
                                                   coop_prob = cp,
                                                   **sn_args)
                                if g == "cra":
                                    growth = sn.growth_cra
                                else:
                                    growth = sn.growth_epa
                                
                                self.start(sn=sn, 
                                           rep=seed[0], 
                                           alg=g, 
                                           growth_method=growth, 
                                           runner=runner, 
                                           selection_method=None,
                                           csv_writer=csvw) 
                fp.flush()
        fp.close()

        
    def start(self, sn, rep, alg, growth_method, runner, 
              selection_method, csv_writer):
        _perf_counter = time.perf_counter()
        
        self.start_network(sn,growth_method)
        if self.GEPHI:
            self.generate_gephi(sn, "initial")

        ave = runner(sn, growth_method, selection_method)
        if self.GEPHI:
            self.generate_gephi(sn, "end")
        
        _perf_counter = round(time.perf_counter() - _perf_counter,2)
        
        if (sn.size != len(sn.g)):
            import ipdb;ipdb.set_trace()
        
        if (sn.cooperators != sn.count_coop()):
            import ipdb;ipdb.set_trace()
        
        csv_writer.writerow((sn.id,rep,sn.network_seed_desc,
                             sn.coop_prob,alg,sn.b,self.X,
                             sn.removed_nodes, sn.gen,
                             sn.cooperators,sn.size,ave,_perf_counter,
                             sn.network_randomseed, sn.randomseed))
    

    def generate_gephi(self, sn, folder):
        gephidir = os.path.join(self.timedir, "gephi", str(sn.id), folder)
        if not os.path.exists(gephidir):
            os.makedirs(gephidir)
        n2g(sn.g, gephidir)
    

    def start_network(self, sn, growth_method):
        GEN = self.GEN
        POP = sn.max

        sn.play_games()
        sn.update_strategies()
        sn.growth_initial(growth_method)
        while (sn.size < POP and sn.gen < GEN):
                sn.play_games()
                sn.update_strategies()
                growth_method()


    def run_without_attrition(self, sn, growth_method, selection_method):    
        GEN = self.GEN
        POP = sn.max
        SAMPLE = self.SAMPLE        
        while (sn.gen <= GEN-SAMPLE):
            sn.play_games()
            sn.update_strategies()
        ave = 0.0
        while (sn.gen < GEN):
            sn.play_games()
            sn.update_strategies()
            ave += sn.cooperators / (1.0 * sn.size)
        #there is something wrong with this average
        sn.play_games()
        sn.update_strategies()
        ave += sn.cooperators / (1.0 * sn.size)
        
        if ave > SAMPLE:
            import ipdb; ipdb.set_trace()
        return ave / SAMPLE

        
    def run_with_attrition(self, sn, growth_method, selection_method):  
        GEN = self.GEN
        POP = sn.max
        SAMPLE = self.SAMPLE
        
        while (sn.gen <= GEN-SAMPLE):
            sn.play_games()
            sn.update_strategies()
            if(sn.size < POP):
                growth_method()
            else:
                sn.attrition(selection_method)  
        ave = 0.0
        while (sn.gen < GEN):
            sn.play_games()
            sn.update_strategies()
            ave += sn.cooperators / (1.0 * sn.size)
            if(sn.size < POP):
                growth_method()
            else:
                sn.attrition(selection_method)     
        #there is something wrong with this average
        sn.play_games()
        sn.update_strategies()
        ave += sn.cooperators / (1.0 * sn.size)
        
        if ave > SAMPLE:
            import ipdb; ipdb.set_trace()
        return ave / SAMPLE

        
    def draw_random(self, sn):
        nx.draw(sn.g)
        plt.show()

        
    def draw(self, sn):
        G=sn.g
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