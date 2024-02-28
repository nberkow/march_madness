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
                nodes_done.add(node)

                # count wins (out-edges) agains un-counted teams
                for w in self.G.out_edges(node):
                    wins += len(set(w).difference(nodes_done))
                    games += len(set(w).difference(nodes_done))

                # count losses (in-edges) agains un-counted teams
                for l in self.G.in_edges(node):
                    games += len(set(l).difference(nodes_done))

                # all neighbors ignoring edge direction
                neighbor_nodes = set(self.G.predecessors(node)).union(set(self.G.neighbors(node)))
                next_layer = next_layer.union(neighbor_nodes)

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
    
    def get_scores_by_tournament_round(self, tournament_path, year):
        with open(tournament_path) as br_file:
            br_reader = csv.reader(br_file)
            tournament = list(br_reader)

        tournament_scores = {}
        tournament_best_rounds = {}
        round = 5
        i = 0

        for g in range(2 ** round):
            game = tournament[g]
            team1, team2 = game
            tournament_scores[team1] = self.neighborhood_search(team1, 4)
            tournament_scores[team2] = self.neighborhood_search(team2, 4)
            tournament_best_rounds[team1] = round
            tournament_best_rounds[team2] = round
            i += 1

        round -= 1
        while round > 0:
            for g in range(2 ** round):
                game = tournament[g+i]
                team1, team2 = game
                tournament_best_rounds[team1] = round
                tournament_best_rounds[team2] = round
                i += 1
            round -= 1

        res = []
        for team in tournament_scores:
            d = [[team, year, tournament_best_rounds[team]] + tournament_scores[team]]
            res.append(d)


if __name__ == "__main__":
    fofg = Friends_Of_Friends_Graph()
    fofg.load_graph("../historical_data/NCAA_Hoops_Results_2022_Final.csv")
    fofg.get_scores_by_tournament_round("../historical_data/2022_results.csv", "2022")