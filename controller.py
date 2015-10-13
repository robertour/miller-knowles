import os
import sys
import time
import csv
import networkx as nx
import powerlaw
from matplotlib import pyplot as plt

from variables import *
from attrition_methods import *
from growth_methods import *
from utils import *

from miller_knowles import *

class ExperimentController():
    
    def __init__(self, 
                 REP = 10, 
                 GEN = 2000, 
                 SAMPLE = 20,
                 GEPHI = False,
                 GRAPHS = False,
                 network_seeds = [TRIAD],
                 coop_probs=[JUST_COOPERATORS], 
                 growths = ["cra","epa"],
                 attritions = [TOURN_LEAST_FIT], 
                 b_s = [1.0,1.3,1.6,1.9,2.2,2.5,2.8],
                 max = 1000,
                 X = [0.025],
                 K = [sys.maxsize],
                 X2 = [0.025]):
        
        
        self.GEN = GEN
        self.REP = REP
        self.PALETTE = get_colormaps(REP)
        self.SAMPLE = SAMPLE
        self.GEPHI = GEPHI
        self.GRAPHS = GRAPHS
        
        self.coop_probs = coop_probs
        self.growths = growths
        self.attritions = attritions

        self.b_s = b_s
        self.max = max
        self.X = X
        self.X2 = X2
        self.K = K
   
        n = int(max*0.95)
        self.seeds = {}
               
        for desc in network_seeds:
            self.seeds[desc] = []
            
            for rep in range(self.REP): 
                st = time.time()
                
                if desc == RANDOM_REGULAR_GRAPH:                    
                    network_seed = nx.random_regular_graph(2,n,seed=st)
                elif desc == ERDOS_RENYI:
                    #network_seed = nx.fast_gnp_random_graph(max,1.0/100,seed=st)
                    # == network_seed = nx.erdos_renyi_graph(1000,0.001,seed=st)                    
                    network_seed = nx.gnm_random_graph(n,2*n,seed=st)
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

                # add the seed to the seeds list                
                self.seeds[desc].append ({'rep': rep,
                                         'nt_seed': network_seed,
                                         'nt_randomseed' : st})

        
        self.timedir = os.path.join("results",time.strftime("%Y%m%d-%H%M%S"))
        if not os.path.exists(self.timedir):
            os.makedirs(self.timedir)


    def run_experiment(self, sn_args_base):
        filename = os.path.join(self.timedir,'fin.csv')
        fp = open(filename, 'w', newline='')
        csvw = csv.writer(fp, delimiter=',')
        csvw.writerow((
                # network descriptors
                'id','rep','network',
                'coop_prob','alg','b','X','K','X2',
                # output measures  
                'removed_nodes', 'gen',
                'cooperators','size','ave','ave2','total_fitness',
                # initial structure measures
                'ini_transitivity','ini_average_clustering',
                'ini_components','ini_size_biggest_component',
                'ini_ave_short_path_biggest',
                # initial fit measures
                'ini_alpha', 'ini_sigma', 'ini_D',
                'ini_xmin', 'ini_xmax',
                'ini_R', 'ini_p',
                # final structure measures 
                'fin_transitivity','fin_average_clustering',
                'fin_components','fin_size_biggest_component',
                'fin_ave_short_path_biggest',
                # final fit measures
                'fin_alpha', 'fin_sigma', 'fin_D',
                'fin_xmin', 'fin_xmax',
                'fin_R', 'fin_p',
                # network seed                
                'network_randomseed', 'randomseed',
                # time measures
                '_ini_perf_counter', '_ini_gephi', 
                '_ini_graphs', '_ini_calcs', '_ini_fit',
                '_fin_perf_counter', '_fin_gephi', 
                '_fin_graphs', '_fin_calcs', '_fin_fit',
                'total_time'))
        fp.flush()

        for desc, seed in self.seeds.items():
            for b in self.b_s:
                for cp in self.coop_probs:
                    for g in self.growths:
                        for att in self.attritions:
                            for x in self.X:
                                for k in self.K:
                                    for x2 in self.X2:
                                        if g == CRA:
                                            growth = growth_cra
                                        elif g == PA:
                                            growth = growth_pa
                                        elif g == EPA:
                                            growth = growth_epa
                                        
                                        fluct = g + "+(" + att +  ")"
                                        if att == TOURN_LEAST_FIT:
                                            att_m = tournament_least_fit
                                        elif att == TOURN_FITTEST:
                                            att_m = tornament_fittest
                                        elif att == LEAST_FIT:
                                            att_m = least_fit
                                        elif att == FITTEST:
                                            att_m = fittest
                                        elif att == RANDOM:
                                            att_m = at_random
                                        elif att == WITHOUT_ATTRITION:
                                            # this is an special case
                                            att_m = None
                                            fluct = g
                                            
                                        att_m2 = tournament_fittest2
                                        
                                        if self.GRAPHS:
                                            # keeps a graph for all the repetitions
                                            fig = plt.figure(2)
                                        
                                        for rep in seed:
                                            sn_args = sn_args_base.copy()
                                            sn_args.update(rep)
                                            
                                            sn = SocialNetwork(fluct=fluct,
                                                               b=b,  
                                                               nt_desc=desc,
                                                               max=self.max,
                                                               X=x,
                                                               K=k,
                                                               X2=x2,
                                                               coop_prob = cp,
                                                               **sn_args)
                                            
                                            self.start(sn=sn,                                                       
                                                       growth_method=growth, 
                                                       att_method=att_m,
                                                       att_method2=att_m2,
                                                       csv_writer=csvw)
                                            
                                            print("Finished:", sn.signature)
                                            
                                            fp.flush()
                                        
                                        if self.GRAPHS:
                                            # after the repetitions are complete
                                            # save the figures
                                            save_figures(sn, 
                                                         self.PALETTE, 
                                                         self.timedir)
                                
        fp.close()

        
    def start(self, sn, growth_method, att_method, att_method2, csv_writer):
        
        total_time = _ini_perf_counter = time.perf_counter()
        self.start_network(sn,growth_method)
        _ini_perf_counter = round(time.perf_counter() - _ini_perf_counter,2)
        
        _ini_calcs = time.perf_counter()            
        initial_nc = network_structure_calculations(sn)
        _ini_calcs = round(time.perf_counter() - _ini_calcs, 2)
        
        _ini_fit = time.perf_counter()
        sn.initial_fit = powerlaw.Fit(sn.degrees, discrete=True)
        sn.initial_comp = sn.initial_fit.distribution_compare('power_law',
                                                              'exponential')
        _ini_fit = round(time.perf_counter() - _ini_fit,2)
        
        _ini_gephi=-1
        if self.GEPHI:
            _ini_gephi = time.perf_counter()
            generate_gephi(sn, self.timedir, FOLDER_INITIAL)
            _ini_gephi = round(time.perf_counter() - _ini_gephi,2)
        _ini_graphs=-1
        if self.GRAPHS:
            _ini_graphs = time.perf_counter()
            generate_graphs(sn, sn.initial_fit, self.timedir, 
                            FOLDER_INITIAL, self.PALETTE)
            _ini_graphs = round(time.perf_counter() - _ini_graphs,2)

        _fin_perf_counter = time.perf_counter()
        (ave, ave2) = self.runner(sn, growth_method, att_method, att_method2)
        _fin_perf_counter = round(time.perf_counter() - _fin_perf_counter,2)
                
        
        if ave == -1:
            sn.cooperators = 0
            total_time = round(time.perf_counter() - total_time,2)
            
            print (""" WARNING: network shrinked completely, this shouldn't
                    happen very often although theoretically it is possible""")
            
            csv_writer.writerow((sn.id,sn.rep,sn.nt_desc,
                                 sn.coop_prob,sn.fluct,sn.b,sn.X,sn.K,sn.X2,
                                 sn.removed_nodes, sn.gen,
                                 sn.cooperators,sn.size,ave,ave2,sn.total_fit,
                                 initial_nc[0],initial_nc[1],initial_nc[2],
                                 initial_nc[3],initial_nc[4],
                                 ini_pw.alpha, ini_pw.sigma, ini_pw.D,
                                 ini_pw.xmin, ini_pw.xmax,
                                 sn.initial_comp[0], sn.initial_comp[1],
                                 -1,-1,-1,
                                 -1,-1,
                                 -1,-1,-1,
                                 -1,-1,
                                 -1,-1,
                                 sn.nt_randomseed, sn.randomseed,
                                 _ini_perf_counter, _ini_gephi, 
                                 _ini_graphs, _ini_calcs, _ini_fit,
                                 -1,-1, 
                                 -1,-1,-1,
                                 total_time))
            
        else: 
            _fin_calcs = time.perf_counter()
            final_nc = network_structure_calculations(sn)
            _fin_calcs = round(time.perf_counter() - _fin_calcs,2)
            
            _fin_fit = time.perf_counter()
            sn.final_fit = powerlaw.Fit(sn.degrees, discrete=True)
            sn.final_comp = sn.final_fit.distribution_compare('power_law', 
                                                              'exponential')
            _fin_fit = round(time.perf_counter() - _fin_fit,2)
            
            _fin_gephi=-1
            if self.GEPHI:
                _fin_gephi = time.perf_counter()
                generate_gephi(sn, self.timedir, FOLDER_FINAL)
                _fin_gephi = round(time.perf_counter() - _fin_gephi,2)
            _fin_graphs=-1
            if self.GRAPHS:
                _fin_graphs = time.perf_counter()
                generate_graphs(sn, sn.final_fit, self.timedir, 
                                FOLDER_FINAL, self.PALETTE)
                _fin_graphs = round(time.perf_counter() - _fin_graphs,2)
            
            if (sn.size != len(sn.g)):
                import ipdb;ipdb.set_trace()
            
            if (sn.cooperators != count_coop(sn)):
                import ipdb;ipdb.set_trace()
                
            total_time = round(time.perf_counter() - total_time,2)
    
            ini_pw = sn.initial_fit.power_law
            fin_pw = sn.final_fit.power_law
            
            csv_writer.writerow((# network descriptors
                                 sn.id,sn.rep,sn.nt_desc,
                                 sn.coop_prob,sn.fluct,sn.b,sn.X,sn.K,sn.X2,
                                 # output measures
                                 sn.removed_nodes, sn.gen,
                                 sn.cooperators,sn.size,ave,ave2,sn.total_fit,
                                 # initial structural measures
                                 initial_nc[0], initial_nc[1],
                                 initial_nc[2], initial_nc[3],
                                 initial_nc[4],
                                 # initial fit measures
                                 ini_pw.alpha, ini_pw.sigma, ini_pw.D,
                                 ini_pw.xmin, ini_pw.xmax,
                                 sn.initial_comp[0], sn.initial_comp[1],
                                 # final structural measures               
                                 final_nc[0], final_nc[1],
                                 final_nc[2], final_nc[3],
                                 final_nc[4],
                                 # final fit measures
                                 fin_pw.alpha, fin_pw.sigma, fin_pw.D,
                                 fin_pw.xmin, fin_pw.xmax,
                                 sn.final_comp[0], sn.final_comp[1],
                                 # seeds
                                 sn.nt_randomseed, sn.randomseed,
                                 # time measures
                                 _ini_perf_counter, _ini_gephi, 
                                 _ini_graphs, _ini_calcs, _ini_fit,
                                 _fin_perf_counter, _fin_gephi, 
                                 _fin_graphs, _fin_calcs, _fin_fit,
                                 total_time))
        

    def start_network(self, sn, growth_method):
        GEN = self.GEN
        POP = sn.max

        sn.play_games_and_remove_isolated_nodes()
        sn.update_strategies()
        sn.growth_initial(growth_method)
        while (sn.size < POP and sn.gen < GEN):
                sn.play_games_and_remove_isolated_nodes()
                sn.update_strategies()
                growth_method(sn)
                #if sn.cooperators > 0:
                #    import ipdb;ipdb.set_trace()

        
    def runner(self, sn, growth_method, att_method, att_method2):  
        GEN = self.GEN
        POP = sn.max
        SAMPLE = self.SAMPLE
        
        while (sn.gen <= GEN-SAMPLE):
            sn.play_games_and_remove_isolated_nodes()
            if sn.size < sn.e_per_gen:
                return (-1, -1)
            sn.update_strategies()
            if(sn.size < POP):
                growth_method(sn)
            else:
                sn.attrition(att_method)
            
            if sn.K > 0 and sn.gen % sn.K == 0:
                sn.attrition(att_method2)

        ave = 0.0
        ave2 = 0.0
        while (sn.gen < GEN):
            sn.play_games_and_remove_isolated_nodes()
            if sn.size < sn.e_per_gen:
                return (-1, -1)
            ave2 += sn.cooperators / (1.0 * sn.size)
            sn.update_strategies()
            ave += sn.cooperators / (1.0 * sn.size)
            if(sn.size < POP):
                growth_method(sn)
            else:
                sn.attrition(att_method)
            
            if sn.K > 0 and sn.gen % sn.K == 0:
                sn.attrition(att_method2)

        sn.play_games_and_remove_isolated_nodes()
        ave2 += sn.cooperators / (1.0 * sn.size)
        sn.update_strategies()
        ave += sn.cooperators / (1.0 * sn.size)
        
        if ave > SAMPLE:
            import ipdb; ipdb.set_trace()

        return (ave / SAMPLE, ave2/SAMPLE)