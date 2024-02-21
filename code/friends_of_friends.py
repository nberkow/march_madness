import networkx as nx
import csv

class Friends_Of_Friends_Graph:

    def __init__(self):
        self.G = nx.MultiDiGraph()

    def load_graph(self, score_path):

        """
        Create an directed unweighted multi-graph.
        Every game is an edge from the winner to the loser
        """

        with open(score_path) as results_file:

            res_csv = csv.reader(results_file)
            next(res_csv, None)

            for res in res_csv:

                team1 = res[3]
                team2 = res[4]

                if res[6] != 'NA' and res[7] != 'NA':
                    score1 = int(res[6])
                    score2 = int(res[7])

                    tie = False
                    if score1 > score2:
                        winner = team1
                        loser = team2

                    elif score2 - score1:
                        winner = team2
                        loser = team1
                    else: 
                        tie = True

                    if not tie:
                        self.G.add_edge(winner, loser)

    def neighborhood_search(self, start_node, layers):

        nodes_done = set()
        layer = set([start_node])
        win_ratios = []

        for i in range(layers):
            wins = 0
            games = 0
            next_layer = set()
            for node in list(layer):
                
                # count winds (out edges) and total games
                g_w = self.G.out_degree(node)
                g_l = self.G.in_degree(node)

                wins += g_w
                games += g_w + g_l

                # all neighbors ignoring edge direction
                neighbor_nodes = set(self.G.predecessors(node)).union(set(self.G.neighbors(node)))
                next_layer = next_layer.union(neighbor_nodes)
                nodes_done.add(node)

                #print(f"{node}\t{wins}\t{games}")

            win_ratios.append(wins/games)
            layer = next_layer.difference(nodes_done)

        return(win_ratios)
    
    def get_scores_for_bracket(self, bracket_path):
        score_ratios_by_team = {}
        with open(bracket_path) as br_file:
            br_reader = csv.reader(br_file)
            for m in range(32):
                matchup = next(br_reader)
                for team in matchup:
                    win_ratios = self.neighborhood_search(team, 4)
                    score_ratios_by_team[team] = win_ratios
        return(score_ratios_by_team)
    
class Friends_Of_Friends_Simulator:

    def __init__(self, bracket_file, win_recs_by_team):
        self.win_recs_by_team = win_recs_by_team
        self.bracket = []

        with open(bracket_file) as brf:
            bracket_reader = csv.reader(brf)
            for i in range(32):
                self.bracket.append(next(bracket_reader))

    def simulate_matchup(self, team_a, team_b):
        team_a_scores = self.win_recs_by_team[team_a]
        team_b_scores = self.win_recs_by_team[team_b]

        total_score = 0
        for i in range(len(team_a_scores)):
            total_score += team_b_scores[i] - team_a_scores[i]

        if total_score >= 0:
            return team_a
        else:
            return team_b
        
    def simulate_tournament(self):

        round = 5
        results = []
        this_round = [i for i in self.bracket[0:64]]

        while round > 0:
            next_round = []
            for i in range(2 ** (round-1)):
                game1, game2 = this_round[i*2:i*2+2]
                winner1 = self.simulate_matchup(game1[0], game1[1])
                winner2 = self.simulate_matchup(game2[0], game2[1])
                next_round.append([winner1, winner2])
            results += next_round
            this_round = next_round
            round -= 1
        results.append([self.simulate_matchup(winner1, winner2),""])

        return self.bracket + results
    
class Bracket_Scorer:

    def __init__(self):
        self.per_round_weight = 2

    def compare_brackets(self, test_bracket, truth_bracket):
        round = 5
        start_idx = 2 ** round
        win_score = self.per_round_weight ** (5-round)

        score_sum = 0

        while round >= 0:
            print(f"round: {round}")
            for g in range(2 ** (round)):
                test_winners = set(test_bracket[start_idx + g])
                truth_winners = set(truth_bracket[start_idx + g])

                print(test_winners)
                print(truth_winners)

                correct = len(test_winners.union(truth_winners))
                score_sum += correct * win_score

                print(correct)
                print(score_sum)

            round -= 1
            start_idx += 2 ** round
            win_score = self.per_round_weight ** (5-round)
        
        return score_sum

        
    def read_bracket_file(self, fname):

        bracket = []
        with open(fname) as bracket_file:
            bracket_reader = csv.reader(bracket_file)
            for game in bracket_reader:
                bracket.append(game)
        return(bracket)

if __name__ == "__main__":

    
    fof = Friends_Of_Friends_Graph()
    fof.load_graph("../historical_data/NCAA_Hoops_Results_2022_Final.csv")
    win_recs = fof.get_scores_for_bracket("../historical_data/2022_results.csv")
    
    sim = Friends_Of_Friends_Simulator("../historical_data/2022_results.csv", win_recs)
    results = sim.simulate_tournament()
    

    scorer = Bracket_Scorer()
    true_results = scorer.read_bracket_file("../historical_data/2022_results.csv")
    s = scorer.compare_brackets(true_results, results)
    print(s)


