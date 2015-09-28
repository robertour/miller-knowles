TOURN_LEAST_FIT = 'TLF'
TOURN_FITTEST = 'TF'
LEAST_FIT = 'LF'
FITTEST = 'F'
AT_RANDOM = 'R'

experiment = { 
  "controller": {
      "REP" : 10,
      "GEN" : 2000,
      "SAMPLE" : 20,
      "attritions" : ['+'],
      "selections" : ['F'],
      "growths" : ["epa"],
      "b_s" : [0.7,1.0,1.3,1.6,1.9,2.2,2.5,2.8]
  },
  "sn" : { 
      "n_per_gen" : 10,
      "e_per_gen" : 2,
      "epsilon" : 0.99,
      "max" : 1000,
      "tourn" : 0.01,
      "X" : 0.025
    }
}