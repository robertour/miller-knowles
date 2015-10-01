from variables import *

experiment = { 
  "controller": {
    "REP" : 10,
    "GEN" : 2000,
    "SAMPLE" : 20,
    "GEPHI": False,
    "network_seeds": [ERDOS_RENYI,
                      BARABASI_ALBERT,
                      RANDOM_REGULAR_GRAPH],
    "coop_probs": [JUST_COOPERATORS,
                   JUST_DEFECTORS,
                   RANDOM_PLAYERS],
    "growths" : [EPA],
    "attritions" : [WITH_ATTRITION,
                    WITHOUT_ATTRITION],
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
