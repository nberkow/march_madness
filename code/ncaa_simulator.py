import datetime
import statistics
import random
import math

class ncaa_simulator:

    def simulate_tournament(self, win_records, bracket):

        print("simulating tournament")
        teams = 64

        for round in range(6):
            new_bracket = []
            for t in range(int(teams/2)):
                team1 = bracket[t * 2]
                team2 = bracket[t * 2 + 1]
                print(f"{team1}\tVS\t{team2}")

                team1_score = statistics.mean(  win_rec[team1][True]["scored"] + \
                                                win_rec[team1][False]["scored"] + \
                                                win_rec[team2][True]["gave"] + \
                                                win_rec[team2][False]["gave"])

                team2_score = statistics.mean(  win_rec[team2][True]["scored"] + \
                                                win_rec[team2][False]["scored"] + \
                                                win_rec[team1][True]["gave"] + \
                                                win_rec[team1][False]["gave"])

                winner = team1
                win_score = team1_score
                loss_score = team2_score
                if team1_score < team2_score:
                    winner = team2    
                    win_score = team2_score
                    loss_score = team1_score

                new_bracket.append(winner)
                print(f"winner:\t{winner}\t{win_score}-{loss_score}")
                print("\n")

            bracket = new_bracket
            teams = teams/2

    def simulate_season(self, win_records):

        contest_set = 150
        contests = self.contest_number
        teams = list(win_records)
        new_win_records = {}

        for contest in range(contests):

            random.shuffle(teams)
            subset1 = teams[0:contest_set]
            subset2 = teams[contest_set:contest_set*2]

            for c in range(contest_set):
                home_game = random.choice([True, False])
                team1 = subset1[c]
                team2 = subset2[c]

                if not team1 in new_win_records:
                    new_win_records[team1] = {
                    True : {"scored" : [], "gave" : [], 
                        "win_scores" : [], "loss_scores" : [], 
                        "op_win_scores" : [], "op_loss_scores" : []},
                    False : {"scored" : [], "gave" : [], 
                        "win_scores" : [], "loss_scores" : [], 
                        "op_win_scores" : [], "op_loss_scores" : []}
                }

                if not team2 in new_win_records:
                    new_win_records[team2] = {
                    True : {"scored" : [], "gave" : [], 
                        "win_scores" : [], "loss_scores" : [], 
                        "op_win_scores" : [], "op_loss_scores" : []},
                    False : {"scored" : [], "gave" : [], 
                        "win_scores" : [], "loss_scores" : [], 
                        "op_win_scores" : [], "op_loss_scores" : []}
                }

                team1_sim_score = statistics.mean(win_rec[team1][home_game]["scored"] + \
                                                  win_rec[team2][not home_game]["gave"]) + \
                                                  random.choice(self.noise)

                team2_sim_score = statistics.mean(win_rec[team1][home_game]["gave"] + \
                                                  win_rec[team2][not home_game]["scored"]) + \
                                                  random.choice(self.noise)


                if team1_sim_score > team2_sim_score:
                    
                    team1_score = statistics.mean(win_rec[team1][home_game]["win_scores"] + \
                                                  win_rec[team2][home_game]["op_win_scores"]) + \
                                                  random.choice(self.noise)

                    team2_score = statistics.mean(win_rec[team2][home_game]["loss_scores"] + \
                                                  win_rec[team1][home_game]["op_loss_scores"]) + \
                                                  random.choice(self.noise)

                    new_win_records[team1][home_game]["win_scores"].append(team1_score)
                    new_win_records[team1][home_game]["op_loss_scores"].append(team2_score)
                    new_win_records[team1][home_game]["scored"].append(team1_score)
                    new_win_records[team1][home_game]["gave"].append(team2_score)

                    new_win_records[team2][not home_game]["loss_scores"].append(team1_score)
                    new_win_records[team2][not home_game]["op_win_scores"].append(team1_score)
                    new_win_records[team2][not home_game]["scored"].append(team2_score)
                    new_win_records[team2][not home_game]["gave"].append(team1_score)

                if team2_sim_score > team1_sim_score:

                    team2_score = statistics.mean(win_rec[team2][not home_game]["win_scores"] + \
                                                  win_rec[team1][not home_game]["op_win_scores"]) + \
                                                  random.choice(self.noise)

                    team1_score = statistics.mean(win_rec[team1][home_game]["loss_scores"] + \
                                                  win_rec[team2][home_game]["op_loss_scores"]) + \
                                                  random.choice(self.noise)

                    new_win_records[team1][home_game]["win_scores"].append(team1_score)
                    new_win_records[team1][home_game]["op_loss_scores"].append(team2_score)
                    new_win_records[team1][home_game]["scored"].append(team1_score)
                    new_win_records[team1][home_game]["gave"].append(team2_score)

                    new_win_records[team2][not home_game]["loss_scores"].append(team1_score)
                    new_win_records[team2][not home_game]["op_win_scores"].append(team1_score)
                    new_win_records[team2][not home_game]["scored"].append(team2_score)
                    new_win_records[team2][not home_game]["gave"].append(team1_score)



        return(new_win_records)

    def bootstrap_first_season(self):

        win_records = {}
        game_count = {}
        self.noise = [0] * 13 + [2] * 7 + [4] * 2 + [6] + [-2] * 7 + [-4] * 2 + [-6]

        for d in self.starting_data:
            team1, team2, location, score1, score2, delta = d

            if not team1 in win_records:
                win_records[team1] = {
                    True : {"scored" : [], "gave" : [], 
                        "win_scores" : [], "loss_scores" : [], 
                        "op_win_scores" : [], "op_loss_scores" : []},
                    False : {"scored" : [], "gave" : [], 
                        "win_scores" : [], "loss_scores" : [], 
                        "op_win_scores" : [], "op_loss_scores" : []}
                }
                game_count[team1] = 0

            if not team2 in win_records:
                win_records[team2] = {
                    True : {"scored" : [], "gave" : [], 
                        "win_scores" : [], "loss_scores" : [], 
                        "op_win_scores" : [], "op_loss_scores" : []},
                    False : {"scored" : [], "gave" : [], 
                        "win_scores" : [], "loss_scores" : [], 
                        "op_win_scores" : [], "op_loss_scores" : []}
                }
                game_count[team2] = 0

            game_count[team1] += 1
            game_count[team2] += 1

            x = 0

            # Add scores, duplicating most recent
            # non-home games count as away

            while x < self.contest_number * (self.delta_decay ** delta):
                win_records[team1][location == 'H']["scored"].append(score1)
                x += random.random()

            x = 0
            while x < self.contest_number * (self.delta_decay ** delta):
                win_records[team1][location == 'H']["gave"].append(score2)
                x += random.random()
                
            x= 0
            while x < self.contest_number * (self.delta_decay ** delta):
                win_records[team2][location != 'H']["scored"].append(score2)
                x += random.random()

            x = 0
            while x < self.contest_number * (self.delta_decay ** delta):
                win_records[team2][location != 'H']["gave"].append(score1)
                x += random.random()

            # count wins and losses. Ignore ties
            if (score1 > score2):

                x = 0
                while x < self.contest_number * (self.delta_decay ** delta):
                    win_records[team1][location == 'H']["win_scores"].append(score1)
                    x += random.random()

                x = 0
                while x < self.contest_number * (self.delta_decay ** delta):
                    win_records[team1][location == 'H']["op_loss_scores"].append(score2)
                    x += random.random()

                x = 0
                while x < self.contest_number * (self.delta_decay ** delta):
                    win_records[team2][location != 'H']["loss_scores"].append(score2)
                    x += random.random()

                x = 0
                while x < self.contest_number * (self.delta_decay ** delta):
                    win_records[team2][location != 'H']["op_win_scores"].append(score1)
                    x += random.random()

            if (score2 > score1):
                x = 0
                while x < self.contest_number * (self.delta_decay ** delta):
                    win_records[team2][location != 'H']["win_scores"].append(score2)
                    x += random.random()

                x = 0
                while x < self.contest_number * (self.delta_decay ** delta):
                    win_records[team2][location != 'H']["op_loss_scores"].append(score1)
                    x += random.random()

                x = 0
                while x < self.contest_number * (self.delta_decay ** delta):
                    win_records[team1][location == 'H']["loss_scores"].append(score1)
                    x += random.random()

                x = 0
                while x < self.contest_number * (self.delta_decay ** delta):
                    win_records[team1][location == 'H']["op_win_scores"].append(score2)
                    x += random.random()

        for t in game_count:
            if game_count[t] < self.min_games:
                win_records.pop(t)
        
        return(win_records)

    def __init__(self, score_file_path):

        self.delta_decay = .95 
        self.contest_number = 60
        self.min_games = 10
        self.tournament_start = datetime.date(2023, 3, 16)
        self.starting_data = []

        with open(score_file_path) as results_file:
            
            self.starting_data = []
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

if __name__ == "__main__":

    sim = ncaa_simulator()
    win_rec = sim.bootstrap_first_season()
    for x in range(5):       
        print(x)
        
    bracket = [
      "team_1_div_1",
      "team16_div_1",
      "team2_div_1",
      "team15_div_1",
      ...
      "team_7_div_4",
      "team_8_div_4",
    ]
    
    sim.simulate_tournament(win_rec, bracket)  
