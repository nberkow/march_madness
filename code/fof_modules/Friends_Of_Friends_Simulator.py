import math
import random
import csv

class Friends_Of_Friends_Simulator:

    def __init__(self, bracket_file, win_recs_by_team):
        self.win_recs_by_team = win_recs_by_team
        self.bracket = []

        with open(bracket_file) as brf:
            bracket_reader = csv.reader(brf)
            for i in range(32):
                self.bracket.append(next(bracket_reader))

    def simulate_matchup(self, team_a, team_b, weights, weighted_flip=True):
        team_a_scores = self.win_recs_by_team[team_a]
        team_b_scores = self.win_recs_by_team[team_b]

        team_a_log_total = 0
        team_b_log_total = 0

        for i in range(len(team_a_scores)):
            team_a_log_total += (math.log(team_a_scores[i]) + math.log(1 - team_b_scores[i])) * weights[i]
            team_b_log_total += (math.log(team_b_scores[i]) + math.log(1 - team_a_scores[i])) * weights[i]

        p_a = math.e ** team_a_log_total
        p_b = math.e ** team_b_log_total
        p = p_a/(p_a + p_b)

        t = 0.5
        if weighted_flip:
            t = random.random()
        
        if p > t:
            return(team_a)
        return(team_b)

    def simulate_tournament(self, weights):

        round = 5
        results = []
        this_round = [i for i in self.bracket[0:64]]

        while round > 0:
            next_round = []
            for i in range(2 ** (round-1)):
                game1, game2 = this_round[i*2:i*2+2]
                winner1 = self.simulate_matchup(game1[0], game1[1], weights)
                winner2 = self.simulate_matchup(game2[0], game2[1], weights)
                next_round.append([winner1, winner2])
            results += next_round
            this_round = next_round
            round -= 1
        results.append([self.simulate_matchup(winner1, winner2, weights),""])

        return self.bracket + results
    