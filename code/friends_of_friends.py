import networkx as nx
import csv
import math
import random
from fof_modules.Friends_Of_Friends_Graph import Friends_Of_Friends_Graph
from fof_modules.Friends_Of_Friends_Simulator import Friends_Of_Friends_Simulator
from Bracket_Scorer import Bracket_Scorer

if __name__ == "__main__":
    
    fof = Friends_Of_Friends_Graph()
    fof.load_graph("../historical_data/NCAA_Hoops_Results_2022_Final.csv")
    win_recs = fof.get_scores_for_bracket("../historical_data/2022_results.csv")
    
    sim = Friends_Of_Friends_Simulator("../historical_data/2022_results.csv", win_recs)
    weights = (1,2,1,2)
    results = sim.simulate_tournament(weights)
    
    scorer = Bracket_Scorer()
    true_results = scorer.read_bracket_file("../historical_data/2022_results.csv")
    s = scorer.compare_brackets(true_results, results)
    print(s)


