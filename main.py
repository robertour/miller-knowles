from controller import ExperimentController
from experiment import experiment

def execute_from_file():     
    ec = ExperimentController(**(experiment["controller"]))
    ec.run_experiment(experiment["sn"])
        
execute_from_file()