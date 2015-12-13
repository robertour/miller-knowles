from variables import *

"""
CAUTION: It is better to test Models without attrition separately because
any attrition with X = 0 or X2 = 0 is equivalent to no attrition.
"""


experiment = {
  "controller": {
    "REP" : 50,
    "GEN" : 2000,
    "SAMPLE" : 20,
    "GEPHI": True,
    "GRAPHS": True,
    "network_seeds": [TRIAD],
    "coop_probs": [JUST_COOPERATORS],
    "growths" : [EPA],
    "attritions" : [TOURN_LEAST_FIT],
    "max" : 1000,
    "b_s" : [1.3,1.6,1.9,2.2,2.5],
    "X" : [0,0.01,0.025],
    "K" : [10], 
    "X2" : [0.001,0.01,0.001]
  },
  "sn" : {
      "n_per_gen" : 10,
      "e_per_gen" : 2,
      "tourn" : 0.01,
      "randomseed" : None,
    }
}



# COOPERATORS 20-10-2015
""" last exectution 
experiment = {
  "controller": {
    "REP" : 10,
    "GEN" : 2000,
    "SAMPLE" : 20,
    "GEPHI": True,
    "GRAPHS": True,
    "network_seeds": [TRIAD],
    "coop_probs": [JUST_DEFECTORS],
    "growths" : [PA,EPA,CRA],
    "attritions" : [TOURN_LEAST_FIT],
    "max" : 1000,
    "b_s" : [1.0],
    "X" : [0,0.01,0.025],
    "K" : [0],#10,20,40,80
    "X2" : [0]
  },
  "sn" : {
      "n_per_gen" : 10,
      "e_per_gen" : 2,
      "tourn" : 0.01,
      "randomseed" : None,
    }
}
"""

# COOPERATORS 19-10-2015
"""
experiment = { 
  "controller": {
    "REP" : 10,
    "GEN" : 2000,
    "SAMPLE" : 20,
    "GEPHI": True,
    "GRAPHS": True,
    "network_seeds": [TRIAD],
    "coop_probs": [JUST_COOPERATORS],
    "growths" : [PA,EPA,CRA],
    "attritions" : [TOURN_LEAST_FIT],
    "max" : 1000,
    "b_s" : [1.3,1.6,1.9,2.2,2.5],
    #"b_s" : [1.6],
    #"b_s" : [1.0,1.5,2.0,2.5],
    #"b_s" : [0.4,0.7,1.0,1.3,1.6],
    "X" : [0,0.01,0.025],
    "K" : [10], 
    "X2" : [0.001,0.01,0.001]
  },
  "sn" : { 
      "n_per_gen" : 10,
      "e_per_gen" : 2,
      "tourn" : 0.01,
      "randomseed" : None,
    }
}
"""


""" DEFECTORS
experiment = { 
  "controller": {
    "REP" : 10,
    "GEN" : 2000,
    "SAMPLE" : 20,
    "GEPHI": True,
    "GRAPHS": True,
    "network_seeds": [TRIAD],
    "coop_probs": [JUST_DEFECTORS],
    "growths" : [PA,EPA,CRA],
    "attritions" : [TOURN_LEAST_FIT],
    "max" : 1000,
    "b_s" : [1.3,1.6,1.9,2.2,2.5],
    #"b_s" : [1.6],
    #"b_s" : [1.0,1.5,2.0,2.5],
    #"b_s" : [0.4,0.7,1.0,1.3,1.6],
    "X" : [0,0.01,0.025],
    "K" : [10,20], 
    "X2" : [0.001,0.01]# leaving ,0.1] out because, 
                       # at least the version with 20 exists
                       # but missing 10 :(
  },
  "sn" : { 
      "n_per_gen" : 10,
      "e_per_gen" : 2,
      "tourn" : 0.01,
      "randomseed" : None,
    }
}
"""

""" MISSING COOPERATORS WITHOUT ATTRITION OF ELITES
experiment = { 
  "controller": {
    "REP" : 10,
    "GEN" : 2000,
    "SAMPLE" : 20,
    "GEPHI": True,
    "GRAPHS": True,
    "network_seeds": [TRIAD],
    "coop_probs": [JUST_COOPERATORS],
    "growths" : [PA,EPA,CRA],
    "attritions" : [TOURN_LEAST_FIT],
    "max" : 1000,
    "b_s" : [1.3,1.6,1.9,2.2,2.5],
    #"b_s" : [1.6],
    #"b_s" : [1.0,1.5,2.0,2.5],
    #"b_s" : [0.4,0.7,1.0,1.3,1.6],
    "X" : [0,0.01,0.025],
    "K" : [0], 
    "X2" : [0]
  },
  "sn" : { 
      "n_per_gen" : 10,
      "e_per_gen" : 2,
      "tourn" : 0.01,
      "randomseed" : None,
    }
}
"""

""" just defectors - no attrition of elites
experiment = { 
  "controller": {
    "REP" : 10,
    "GEN" : 2000,
    "SAMPLE" : 20,
    "GEPHI": True,
    "GRAPHS": True,
    "network_seeds": [TRIAD],
    "coop_probs": [JUST_DEFECTORS],
    "growths" : [PA,EPA,CRA],
    "attritions" : [TOURN_LEAST_FIT],
    "max" : 1000,
    "b_s" : [1.3,1.6,1.9,2.2,2.5],
    #"b_s" : [1.6],
    #"b_s" : [1.0,1.5,2.0,2.5],
    #"b_s" : [0.4,0.7,1.0,1.3,1.6],
    "X" : [0,0.01,0.025],
    "K" : [0], 
    "X2" : [0]
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
    "REP" : 10,
    "GEN" : 2000,
    "SAMPLE" : 20,
    "GEPHI": True,
    "GRAPHS": True,
    "network_seeds": [TRIAD],
    "coop_probs": [JUST_DEFECTORS],
    "growths" : [PA,EPA,CRA],
    "attritions" : [TOURN_LEAST_FIT],
    "max" : 1000,
    "b_s" : [1.3,1.6,1.9,2.2,2.5],
    #"b_s" : [1.6],
    #"b_s" : [1.0,1.5,2.0,2.5],
    #"b_s" : [0.4,0.7,1.0,1.3,1.6],
    "X" : [0,0.01,0.025],
    "K" : [10,20], 
    "X2" : [0.001,0.01,0.1]
  },
  "sn" : { 
      "n_per_gen" : 10,
      "e_per_gen" : 2,
      "tourn" : 0.01,
      "randomseed" : None,
    }
}
"""



""" full attrition
experiment = { 
  "controller": {
    "REP" : 10,
    "GEN" : 2000,
    "SAMPLE" : 20,
    "GEPHI": False,
    "GRAPHS": False,
    "network_seeds": [TRIAD],
    "coop_probs": [JUST_DEFECTORS,JUST_COOPERATORS],
    "growths" : [PA,EPA,CRA],
    "attritions" : [TOURN_LEAST_FIT],
    "max" : 1000,
    #"b_s" : [1.6,1.9,2.2,2.5],
    #"b_s" : [1.6],
    "b_s" : [1.3,1.6,1.9,2.2,2.5],
    #"b_s" : [0.4,0.7,1.0,1.3,1.6],
    "X" : [0,0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9],
    "K" : [0],
    "X2" : [0]
  },
  "sn" : { 
      "n_per_gen" : 10,
      "e_per_gen" : 2,
      "tourn" : 0.01,
      "randomseed" : None,
    }
}
"""

""" this was running the missing baselines
experiment = { 
  "controller": {
    "REP" : 10,
    "GEN" : 2000,
    "SAMPLE" : 20,
    "GEPHI": False,
    "GRAPHS": False,
    "network_seeds": [TRIAD],
    "coop_probs": [JUST_DEFECTORS,JUST_COOPERATORS],
    "growths" : [PA,EPA,CRA],
    "attritions" : [TOURN_LEAST_FIT],
    "max" : 1000,
    #"b_s" : [1.6,1.9,2.2,2.5],
    #"b_s" : [1.6],
    "b_s" : [1.3,1.6,1.9,2.2,2.5],
    #"b_s" : [0.4,0.7,1.0,1.3,1.6],
    "X" : [0],
    "K" : [0],
    "X2" : [0]
  },
  "sn" : { 
      "n_per_gen" : 10,
      "e_per_gen" : 2,
      "tourn" : 0.01,
      "randomseed" : None,
    }
}
"""

""" THIS IS WITH THE NEW ATTRITION
experiment = { 
  "controller": {
    "REP" : 10,
    "GEN" : 2000,
    "SAMPLE" : 20,
    "GEPHI": False,
    "GRAPHS": False,
    "network_seeds": [TRIAD],
    "coop_probs": [JUST_DEFECTORS,JUST_COOPERATORS],
    "growths" : [PA,EPA,CRA],
    "attritions" : [TOURN_LEAST_FIT],
    "max" : 1000,
    #"b_s" : [1.6,1.9,2.2,2.5],
    #"b_s" : [1.6],
    "b_s" : [1.0,1.5,2.0,2.5],
    #"b_s" : [0.4,0.7,1.0,1.3,1.6],
    "X" : [0,0.025],
    "K" : [10,100,1000],
    "X2" : [0,0.001,0.1]
  },
  "sn" : { 
      "n_per_gen" : 10,
      "e_per_gen" : 2,
      "tourn" : 0.01,
      "randomseed" : None,
    }
}
"""

""" 50 % attritions
experiment = { 
  "controller": {
    "REP" : 10,
    "GEN" : 2000,
    "SAMPLE" : 20,
    "GEPHI": False,
    "GRAPHS": False,
    "network_seeds": [TRIAD],
    "coop_probs": [RANDOM_PLAYERS],
    "growths" : [PA,EPA,CRA],
    "attritions" : [WITHOUT_ATTRITION,
                    TOURN_LEAST_FIT],
    "max" : 1000,
    #"b_s" : [1.6,1.9,2.2,2.5],
    #"b_s" : [1.6],
    "b_s" : [1.0,1.5,2.0,2.5,3.0],
    #"b_s" : [0.4,0.7,1.0,1.3,1.6],
    "X" : [0.5]
  },
  "sn" : { 
      "n_per_gen" : 10,
      "e_per_gen" : 2,
      "tourn" : 0.01,
      "randomseed" : None,
    }
}
"""

""" with the graphs, gephi and pa
experiment = { 
  "controller": {
    "REP" : 10,
    "GEN" : 2000,
    "SAMPLE" : 20,
    "GEPHI": True,
    "GRAPHS": True,
    "network_seeds": [TRIAD],
    "coop_probs": [JUST_COOPERATORS, 
                    RANDOM_PLAYERS,
                    JUST_DEFECTORS],
    "growths" : [PA,EPA,CRA],
    "attritions" : [WITHOUT_ATTRITION,
                    TOURN_LEAST_FIT],
    "max" : 1000,
    #"b_s" : [1.6,1.9,2.2,2.5],
    #"b_s" : [1.6],
    "b_s" : [1.5,2.0,2.5,3.0,1.0],
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

""" repeate miller
experiment = { 
  "controller": {
    "REP" : 10,
    "GEN" : 2000,
    "SAMPLE" : 20,
    "GEPHI": False,
    "network_seeds": [TRIAD],
    "coop_probs": [JUST_COOPERATORS, JUST_DEFECTORS],
    "growths" : [EPA,CRA],
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


""" measuring attritions
experiment = { 
  "controller": {
    "REP" : 10,
    "GEN" : 2000,
    "SAMPLE" : 20,
    "GEPHI": False,
    "network_seeds": [TRIAD],
    "coop_probs": [RANDOM_PLAYERS],
    "growths" : [EPA,
                 CRA],
    "attritions" : [WITH_ATTRITION,
                    WITHOUT_ATTRITION],
    "selections" : [RANDOM,
                    TOURN_LEAST_FIT],
    "max" : 1000,
    #"b_s" : [1.6,1.9,2.2,2.5],
    #"b_s" : [1.0,1.3,1.6,1.9,2.2],
    "b_s" : [1.0,1.5,2.0,2.5,3.0],
    #"b_s" : [0.4,0.7,1.0,1.3,1.6],
    "X" : [0.005, 0.001]
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