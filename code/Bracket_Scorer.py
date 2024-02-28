import csv

class Bracket_Scorer:

    def __init__(self):
        self.per_round_weight = 2

    def compare_brackets(self, truth_bracket, test_bracket):

        round = 5
        start_idx = 2 ** round

        win_score = self.per_round_weight ** (5-round)
        score_sum = 0

        while round > 0:
            round -= 1
            for g in range(2 ** (round)):

                test_winners = set(test_bracket[start_idx + g])
                truth_winners = set(truth_bracket[start_idx + g])

                correct = len(test_winners.intersection(truth_winners))
                score_sum += correct * win_score

            start_idx += 2 ** round
            win_score = self.per_round_weight ** (5-round)
        
        test_champ = set(test_bracket[-1])
        truth_champ = set(test_bracket[-1])
        score_sum += len(test_champ.intersection(truth_champ) - set([""])) * self.per_round_weight ** 5
        
        return score_sum
        
    def read_bracket_file(self, fname):

        bracket = []
        with open(fname) as bracket_file:
            bracket_reader = csv.reader(bracket_file)
            for game in bracket_reader:
                bracket.append(game)
        return(bracket)