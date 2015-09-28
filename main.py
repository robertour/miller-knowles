from controller import ExperimentController
from experiment import experiment

       
def execute_from_file(filename = "experiment.dict"):     
    ec = ExperimentController(**(experiment["controller"]))
    ec.run_experiment(experiment["sn"])
        
execute_from_file("experiment.dict")