from variables import *

experiment = { 
  "controller": {
    "REP" : 10,
    "GEN" : 2000,
    "SAMPLE" : 20,
    "GEPHI": False,
    "network_seeds": [TRIAD],
    "coop_probs": [JUST_DEFECTORS],
    "growths" : [CRA],
    "attritions" : [WITHOUT_ATTRITION],
    "selections" : [LEAST_FIT,
                    TOURN_LEAST_FIT,
                    RANDOM],
    "max" : 1000,
    #"b_s" : [1.0,1.3,1.6,1.9,2.2],
    "b_s" : [0.4,0.7,1.0,1.3,1.6],
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