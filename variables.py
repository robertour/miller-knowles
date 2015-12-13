# Estrategies
COOP = 'C'
DEFE = 'D'
strategies = [COOP, DEFE]

# Probability of a node being a cooperator
JUST_COOPERATORS = 1.0
JUST_DEFECTORS = 0.0
RANDOM_PLAYERS = 0.5

# Mechanisms of selection of attrtition
TOURN_LEAST_FIT = 'TLF'
TOURN_FITTEST = 'TF'
LEAST_FIT = 'LF'
FITTEST = 'F'
RANDOM = 'R'
WITHOUT_ATTRITION = ''

# Types of starting networks 
RANDOM_REGULAR_GRAPH = 'RRG'
ERDOS_RENYI = 'ER'
BARABASI_ALBERT = 'BA'
WATTS_STROGATZ = 'WS'
TRIAD = 'TRIAD'

# Types of growth
EPA = "epa"
CRA = "cra"
PA = "pa"


CCDF = 0
CCDF_INITIAL = 1
CCDF_FINAL = 2

PDF = 3
PDF_INITIAL = 4
PDF_FINAL = 5

DR = 6
DR_INITIAL = 7
DR_FINAL = 8

DFD = 9
DFD_INITIAL = 10
DFD_FINAL = 11

INITIAL_STAGE = 0
FINAL_STAGE = 1

FOLDER_INITIAL = 'initial'
FOLDER_FINAL = 'final'

COLS_DESCRIPTORS = (
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
                'total_time')

COLS_DESCRIPTORS_ITER = (
                # network descriptors
                'id','rep','network',
                'coop_prob','alg','b','X','K','X2',
                # output measures  
                'removed_nodes', 'gen',
                'cooperators','size','ave','ave2','total_fitness',
                # network seed                
                'network_randomseed', 'randomseed')