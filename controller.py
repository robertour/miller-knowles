import json
import os
import time
import timeit
import csv
import random
import networkx as nx
import powerlaw

from variables import *
from selection_methods import *

from miller_knowles import *
from networkx_to_gephi import n2g
from networkx.generators.random_graphs import gnm_random_graph
from networkx.algorithms.cluster import triangles, transitivity, clustering,\
    average_clustering
from networkx.algorithms.shortest_paths.generic import \
    average_shortest_path_length



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
    
        n = int(max*0.95)
        self.seeds = []
        for rep in range(self.REP):        
            for desc in network_seeds:
                st = time.time()
                
                if desc == RANDOM_REGULAR_GRAPH:                    
                    network_seed = nx.random_regular_graph(2,n,seed=st)
                elif desc == ERDOS_RENYI:
                    #network_seed = nx.fast_gnp_random_graph(max,1.0/100,seed=st)
                    # == network_seed = nx.erdos_renyi_graph(1000,0.001,seed=st)                    
                    network_seed = gnm_random_graph(n,2*n,seed=st)
                elif desc == BARABASI_ALBERT:
                    network_seed = nx.barabasi_albert_graph(n,2,seed=st)
                elif desc == WATTS_STROGATZ:
                    # according to wikipedia N >> K >> ln(1000) >> 0.001
                    # network_seed = 
                    # nx.newman_watts_strogatz_graph(1000, 14, 0.001,seed=st)
                    # 7000 edges
                    network_seed = nx.watts_strogatz_graph(n, 14, 0.01,seed=st) 
                elif desc == TRIAD:
                    network_seed = nx.random_regular_graph(2,3,seed=st)
                else:
                    raise ValueError('Not recognized seed')

#                 centrality_dict = nx.degree_centrality(network_seed)
#                 centrality_list = list(centrality_dict.values())
#                 centrality_array = np.array(centrality_list)
#                 centrality_not_norm = centrality_array * 999
#                 centrality_int = centrality_not_norm.astype(int)
#                 results = powerlaw.Fit(centrality_int.tolist())
                
                #self.plot_degree_distribution(network_seed)

                #import ipdb; ipdb.set_trace()
                    
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
               'cooperators','size','ave','ave2','total_fitness',
               'ini_transitivity','ini_average_clustering',
               'ini_components','ini_size_biggest_component',
               'ini_ave_short_path_biggest',                       
               'fin_transitivity','fin_average_clustering',
               'fin_components','fin_size_biggest_component',
               'fin_ave_short_path_biggest',                       
               'network_randomseed', 'randomseed',
               'real_time'))
        fp.flush()

        for seed in self.seeds:
            for b in self.b_s:
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
                                            selection = tornament_least_fit
                                        elif s == TOURN_FITTEST:
                                            selection = tornament_fittest
                                        elif s == LEAST_FIT:
                                            selection = least_fit
                                        elif s == FITTEST:
                                            selection = fittest
                                        else:
                                            selection = at_random
                                                              
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
            
        initial_nc = self.network_structure_calculations(rep, alg, sn)

        (ave, ave2) = runner(sn, growth_method, selection_method)
        if self.GEPHI:
            self.generate_gephi(sn, "end")
        
        _perf_counter = round(time.perf_counter() - _perf_counter,2)
        
        
        final_nc = (-1,-1,-1,-1,-1)
        
        if ave == -1:
            sn.cooperators = 0
        else: 
            if (sn.size != len(sn.g)):
                import ipdb;ipdb.set_trace()
            
            if (sn.cooperators != sn.count_coop()):
                import ipdb;ipdb.set_trace()
                
            final_nc = self.network_structure_calculations(rep, alg, sn)

            
        csv_writer.writerow((sn.id,rep,sn.network_seed_desc,
                             sn.coop_prob,alg,sn.b,sn.X,
                             sn.removed_nodes, sn.gen,
                             sn.cooperators,sn.size,ave,ave2,sn.total_fit,
                             initial_nc[0],initial_nc[1],initial_nc[2],
                             initial_nc[3],initial_nc[4],
                             final_nc[0],final_nc[1],final_nc[2],
                             final_nc[3],final_nc[4],
                             sn.network_randomseed, sn.randomseed,
                             _perf_counter))
        


    def network_structure_calculations(self, rep, alg, sn):
        time_of_calcs = time.time()

        g = sn.g

        _transitivity = transitivity(g)
        _average_clustering = average_clustering(g)   
        size_biggest_component = -1
        connected_components = 0
        ave_short_path_biggest = -1
        
        for sg in nx.connected_component_subgraphs(g, False):
            connected_components += 1
            if len(sg) > size_biggest_component:
                size_biggest_component = len(sg)
                ave_short_path_biggest = average_shortest_path_length(sg)
                
        print (rep,sn.network_seed_desc,alg," - final calculations took", (time.time()-time_of_calcs))

        return (_transitivity,_average_clustering,
                connected_components, size_biggest_component,
                ave_short_path_biggest)



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
                #if sn.cooperators > 0:
                #    import ipdb;ipdb.set_trace()


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
        return (ave / SAMPLE, ave / SAMPLE)

        
    def run_with_attrition(self, sn, growth_method, selection_method):  
        GEN = self.GEN
        POP = sn.max
        SAMPLE = self.SAMPLE
        
        while (sn.gen <= GEN-SAMPLE):
            sn.play_games()
            if sn.size < sn.e_per_gen:
                return (-1, -1)
            sn.update_strategies()
            if(sn.size < POP):
                growth_method()
            else:
                sn.attrition(selection_method)

        ave = 0.0
        ave2 = 0.0
        while (sn.gen < GEN):
            sn.play_games()
            if sn.size < sn.e_per_gen:
                return (-1, -1)
            ave2 += sn.cooperators / (1.0 * sn.size)
            sn.update_strategies()
            ave += sn.cooperators / (1.0 * sn.size)
            if(sn.size < POP):
                growth_method()
            else:
                sn.attrition(selection_method)

        sn.play_games()
        ave2 += sn.cooperators / (1.0 * sn.size)
        sn.update_strategies()
        ave += sn.cooperators / (1.0 * sn.size)
        
        if ave > SAMPLE:
            import ipdb; ipdb.set_trace()

        return (ave / SAMPLE, ave2/SAMPLE)

        
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
        
    def plot_degree_distribution(self, G):

        degree_sequence=sorted(nx.degree(G).values(),reverse=True) # degree sequence
        #print "Degree sequence", degree_sequence
        dmax=max(degree_sequence)
        
        plt.loglog(degree_sequence,'b-',marker='o')
        plt.title("Degree rank plot")
        plt.ylabel("degree")
        plt.xlabel("rank")
        
        # draw graph in inset
#         plt.axes([0.45,0.45,0.45,0.45])
#         Gcc=sorted(nx.connected_component_subgraphs(G), key = len, reverse=True)[0]
#         pos=nx.spring_layout(Gcc)
#         plt.axis('off')
#         nx.draw_networkx_nodes(Gcc,pos,node_size=20)
#         nx.draw_networkx_edges(Gcc,pos,alpha=0.4)
        
        plt.savefig("degree_histogram.png")
        plt.show()