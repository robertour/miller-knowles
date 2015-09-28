import json
import os
import time
import timeit
import csv

from experiment import *

from miller_knowles import SocialNetwork

class ExperimentController():
    
    def __init__(self, 
                 REP = 10, 
                 GEN = 2000, 
                 SAMPLE = 20,
                 attritions = [False, True],
                 selections = [TOURN_LEAST_FIT], 
                 growths = ["cra","epa"],
                 b_s = [1.0,1.3,1.6,1.9,2.2,2.5,2.8]):
        
        self.GEN = GEN
        self.REP = REP
        self.SAMPLE = SAMPLE
        self.growths = growths
        self.selections = selections
        self.attritions = []
        # it has to be copied like this if not I get ([False, True],)
        for att in attritions:
            self.attritions.append(att)
        self.b_s = b_s
    
        self.timedir = os.path.join("results",time.strftime("%Y%m%d-%H%M%S"))
        if not os.path.exists(self.timedir):
            os.makedirs(self.timedir)

    def run_experiment(self, sn_args):
        filename = os.path.join(self.timedir,'fin.csv')
        fp = open(filename, 'w', newline='')
        csvw = csv.writer(fp, delimiter=',')
        csvw.writerow(['it', 'alg',"b","coop1","coop2","coop3","tot",
                       "ave1","ave2","d1","d2","d3"])
        fp.flush()


        for rep in range(self.REP):
            for b in self.b_s:
                for att in self.attritions:
                    if att == '+':
                        runner = self.run_with_attrition
                        for g in self.growths:
                            for s in self.selections:
                                sn = SocialNetwork(b, **sn_args)
                                
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
                                
                                self.start(sn, rep, g + att + "(" + s + ")", 
                                           growth, runner, selection, csvw) 
                    else:
                        runner = self.run_without_attrition
                        for g in self.growths:
                            sn = SocialNetwork(b, **sn_args)
                            if g == "cra":
                                growth = sn.growth_cra
                            else:
                                growth = sn.growth_epa
                            
                            self.start(sn, rep, g, growth, runner, 
                                None, csvw) 
                    
                fp.flush()
        fp.close()

        
    
    def start(self, sn, rep, id, growth_method, runner, 
              selection_method, csv_writer):
        _time = time.time()
        _perf_counter = time.perf_counter()
        _process_time = time.process_time()
        
        (ave1, ave2) = runner(sn, growth_method, selection_method)
        
        coop1 = sn.cooperators
        coop2 = sn.count_coop()
        sn.play_games()
        sn.update_strategies()
        coop3 = sn.cooperators
        
        _time = round(time.time() - _time, 2)
        _perf_counter = round(time.perf_counter() - _perf_counter,2)
        _process_time = round(time.process_time() - _process_time,2)
        
        if (sn.size != len(sn.g)):
            import ipdb;ipdb.set_trace()
        
        csv_writer.writerow([rep,id,sn.b,coop1,coop2,coop3,sn.size,ave1,ave2,
                             _time,_perf_counter,_process_time])
    
    
    def run_without_attrition(self, sn, growth_method, selection = None):
        GEN = self.GEN
        REP = self.REP
        SAMPLE = self.SAMPLE
        POP = sn.max
        
        sn.play_games()
        sn.update_strategies()
        sn.growth_initial(growth_method)
                
        while (sn.size < POP and sn.gen < GEN):
            sn.play_games()
            sn.update_strategies()
            growth_method()
        while (sn.gen < GEN-SAMPLE):
            sn.play_games()
            sn.update_strategies()
        ave1 = 0.0
        ave2 = 0.0
        while (sn.gen < GEN):
            sn.play_games()
            sn.update_strategies()
            ave1 += sn.count_coop() / (1.0 * sn.size)
            ave2 += sn.count_coop() / (1.0 * sn.size)

        return (ave1 / SAMPLE, ave2 / SAMPLE)
    
    
    def run_with_attrition(self, sn, growth_method, selection_method):
        GEN = self.GEN
        REP = self.REP
        SAMPLE = self.SAMPLE
        POP = sn.max
        
        sn.play_games()
        sn.update_strategies()
        sn.growth_initial(growth_method)
        
        while (sn.size < POP and sn.gen < GEN):
            sn.play_games()
            sn.update_strategies()
            growth_method()
        while (sn.gen < GEN-SAMPLE):
            sn.play_games()
            sn.update_strategies()
            if(sn.size < POP):
                growth_method()
            else:
                sn.attrition(selection_method)
        ave1 = 0.0
        ave2 = 0.0
        while (sn.gen < GEN):
            sn.play_games()
            sn.update_strategies()
            ave1 += sn.count_coop() / (1.0 * sn.size)
            if(sn.size < POP):
                growth_method()
            else:
                sn.attrition(selection_method)
            ave2 += sn.count_coop() / (1.0 * sn.size)        
        
        return (ave1 / SAMPLE, ave2 / SAMPLE)
        
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