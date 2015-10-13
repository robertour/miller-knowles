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

PDF_CCDF = 0
PDF_INITIAL = 1
CCDF_INITIAL = 2
PDF_FINAL = 3
CCDF_FINAL = 4
DR = 5
DR_INITIAL = 6
DR_FINAL = 7
DFD = 8
DFD_INITIAL = 9
DFD_FINAL = 10

FOLDER_INITIAL = 'initial'
FOLDER_FINAL = 'final'