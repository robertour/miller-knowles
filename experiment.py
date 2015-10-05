from variables import *

experiment = { 
  "controller": {
    "REP" : 10,
    "GEN" : 2000,
    "SAMPLE" : 20,
    "GEPHI": False,
    "network_seeds": [TRIAD],
    "coop_probs": [JUST_DEFECTORS],
    "growths" : [EPA],
    "attritions" : [WITH_ATTRITION,
                    WITHOUT_ATTRITION],
    "selections" : [TOURN_LEAST_FIT],
    "max" : 1000,
    #"b_s" : [1.6,1.9,2.2,2.5],
    "b_s" : [1.0,1.3,1.6,1.9,2.2],
    #"b_s" : [1.0,1.5,2.0,2.5,3.0],
    #"b_s" : [0.4,0.7,1.0,1.3,1.6],
    "X" : [0.025]
  },
  "sn" : { 
      "n_per_gen" : 10,
      "e_per_gen" : 2,
      "tourn" : 0.01,
      "randomseed" : None,
    }
}



"""
experiment = { 
  "controller": {
    "REP" : 10,
    "GEN" : 2000,
    "SAMPLE" : 20,
    "GEPHI": False,
    "network_seeds": [RANDOM_REGULAR_GRAPH,
                      BARABASI_ALBERT,
                      ERDOS_RENYI],
    "coop_probs": [RANDOM_PLAYERS],
    "growths" : [EPA],
    "attritions" : [WITH_ATTRITION,
                    WITHOUT_ATTRITION],
    "selections" : [RANDOM,
                    TOURN_LEAST_FIT],
    "max" : 1000,
    #"b_s" : [1.6,1.9,2.2,2.5],
    #"b_s" : [1.0,1.3,1.6,1.9,2.2],
    "b_s" : [1.0,1.5,2.0,2.5,3.0],
    #"b_s" : [0.4,0.7,1.0,1.3,1.6],
    "X" : [0.001, 0.005]
  },
  "sn" : { 
      "n_per_gen" : 10,
      "e_per_gen" : 2,
      "tourn" : 0.01,
      "randomseed" : None,
    }
}
"""

"""
experiment = { 
  "controller": {
    "REP" : 1,
    "GEN" : 2000,
    "SAMPLE" : 20,
    "GEPHI": False,
    "network_seeds": [TRIAD,
                      ERDOS_RENYI,
                      BARABASI_ALBERT,
                      RANDOM_REGULAR_GRAPH],
    "coop_probs": [JUST_DEFECTORS,
                    JUST_COOPERATORS,
                    RANDOM_PLAYERS],
    "growths" : [CRA, EPA],
    "attritions" : [WITH_ATTRITION, WITHOUT_ATTRITION],
    "selections" : [LEAST_FIT,
                    TOURN_LEAST_FIT,
                    RANDOM],
    "max" : 1000,
    #"b_s" : [1.6,1.9,2.2,2.5],
    "b_s" : [1.0,1.3,1.6,1.9,2.2],
    #"b_s" : [0.4,0.7,1.0,1.3,1.6],
    "X" : [0.01,0.025,0.05]
  },
  "sn" : { 
      "n_per_gen" : 10,
      "e_per_gen" : 2,
      "tourn" : 0.01,
      "randomseed" : None,
    }
}
"""

"""
october 1st analysis
experiment = { 
  "controller": {
    "REP" : 10,
    "GEN" : 2000,
    "SAMPLE" : 20,
    "GEPHI": False,
    "network_seeds": [ERDOS_RENYI],
    "coop_probs": [JUST_COOPERATORS],
    "growths" : [EPA],
    "attritions" : [WITHOUT_ATTRITION],
    "selections" : [LEAST_FIT,
                    TOURN_LEAST_FIT,
                    RANDOM],
    "max" : 1000,
    "b_s" : [1.3,1.6,1.9,2.2,2.5],
    "X" : [0.025]
  },
  "sn" : { 
      "n_per_gen" : 10,
      "e_per_gen" : 2,
      "tourn" : 0.01
    }
}
"""