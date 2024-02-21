import sys
import math
import random
import networkx as nx
import datetime

class ball_lightning:

    def __init__(self):
        self.G = nx.MultiDiGraph()
        self.starting_data = []
        self.recency_decay = .95 # older games don't count as much
        p = .95
        self.home_team_penalty = {True : p, False : 1/p} # home team wins don't count as much
        self.score_diff_base = 1.1
        self.tournament_start = datetime.date(2023, 3, 16)
        self.team_strength = {}

    def simulate_tournament(self, bracket_file):
        
        bracket = []
        print("simulating tournament")
        teams = 64
        with open(bracket_file) as bfl:
            for t in bfl:
                bracket.append(t.rstrip())

        for round in range(6):
            new_bracket = []
            for t in range(int(teams/2)):
                team1 = bracket[t * 2]
                team2 = bracket[t * 2 + 1]
                print(f"{team1}\tVS\t{team2}")
                team1_win_path, team1_win_score = self.find_path_to_dest(team1, team2, 100, 15)
                team2_win_path, team2_win_score = self.find_path_to_dest(team2, team1, 100, 15)

                if team2_win_score * len(team2_win_path) > team1_win_score * len(team1_win_path):
                    print(f"WINNER:\t{team2}")
                    new_bracket.append(team2)

                else:
                    print(f"WINNER:\t{team1}")
                    new_bracket.append(team1)

                print("\n")
            bracket = new_bracket

            teams = int(teams/2)


    def find_path_to_dest(self, team1, team2, max_attempts, max_steps):

        # random walk
        attempts = 0
        edge_to_dest = False
        path_edges = set()

        while attempts < max_attempts and not edge_to_dest:

            steps = 0
            nodes_visited = set()
            working_path = []
            
            path_weight_sum = 0
            source = team1

            while steps < max_steps and not edge_to_dest:
        
                edges = list(self.G.out_edges(source, data=True))
                random.shuffle(edges)
                edge_to_dest = self.check_for_dest(edges, team2)

                if not edge_to_dest:
                    next_edge = self.choose_next_hop(edges, nodes_visited)
                    if next_edge:
                        source = next_edge[1]
                        working_path.append(next_edge)
                        nodes_visited.add(next_edge[1])
                        path_weight_sum += next_edge[2]["weight"]
                    else:
                        steps = max_steps

                else:
                    working_path.append(edge_to_dest[1])
                    path_weight_sum += edge_to_dest[2]["weight"]

                steps += 1

            if edge_to_dest:
                return(working_path, path_weight_sum)
            
            attempts += 1
        return([], 0)

    def check_for_dest(self, edges, dest):

        dest_found = False
        i = 0
        while i < len(edges) and not dest_found:
            e = edges[i]
            if e[1] == dest:
                dest_found = True
            i += 1

        if dest_found:
            return(e)
        else:
            return(False)

    def choose_next_hop(self, edges, nodes_visited):

        valid_hop_found = False
        i = 0
        while i < len(edges) and not valid_hop_found:
            e = edges[i]
            if e[1] not in nodes_visited:
                valid_hop_found = True
            i += 1

        if valid_hop_found:
            return(e)
        else:
            return(False)

            

    def load_data(self, score_path):

        with open(score_path) as results_file:
            
            results_file.readline()
            for res in results_file:
                elts = res.rstrip().split(",")
                year, month, day = elts[0:3]
                d = datetime.date(int(year), int(month), int(day))
                delta = (self.tournament_start - d).days

                team1 = elts[3][1:-1]
                team2 = elts[4][1:-1]

                location = elts[5][1]

                if elts[6] != 'NA' and elts[7] != 'NA':
                    score1 = int(elts[6])
                    score2 = int(elts[7])

                    self.starting_data.append([team1, team2, location, score1, score2, delta])

    def compute_team_strength(self):

        win_counts = {}
        game_counts = {}

        for d in self.starting_data:
            team1, team2, location, score1, score2, delta = d

            if not team1 in win_counts:
                win_counts[team1] = 1
                game_counts[team1] = 1

            if not team2 in win_counts:
                win_counts[team2] = 1
                game_counts[team2] = 1

            game_counts[team1] += self.recency_decay ** delta
            game_counts[team2] += self.recency_decay ** delta

            if (score1 > score2):
                win_counts[team1] += self.recency_decay ** delta

            if (score2 > score1):
                win_counts[team2] += self.recency_decay ** delta

        for team in win_counts:
            self.team_strength[team] = win_counts[team]/game_counts[team]


    def build_graph(self):

        """
        assign edge weights. 
        a higher weight means a more extreme, more recent upset  
        """

        for d in self.starting_data:
            team1, team2, location, score1, score2, delta = d

            tie = False
            if score1 > score2:
                winner = team1
                loser = team2
                score_diff = score1 - score2
                htp = self.home_team_penalty[location == 'H']
            elif score2 - score1:
                winner = team2
                loser = team1
                score_diff = score2 - score1
                htp = self.home_team_penalty[location != 'H']
            else: 
                tie = True
            
            if not tie:
                w = (self.recency_decay ** delta) * htp * (self.score_diff_base ** score_diff)
                w = w * (self.team_strength[loser]/self.team_strength[winner])
                self.G.add_edge(winner, loser, weight=w)
                        

if __name__ == "__main__":

    seed, win_record_file, bracket_file = int(sys.argv[1]), sys.argv[2], sys.argv[3]
    random.seed(seed)

    ball = ball_lightning()
    ball.load_data(win_record_file)
    ball.compute_team_strength()
    ball.build_graph()
    ball.simulate_tournament(bracket_file)

