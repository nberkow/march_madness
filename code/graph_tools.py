from datetime import datetime

class graph_node:
    def __init__(self):
        self.node_id = 'NA'
        self.edges = []

class graph_edge:
    def __init__(self, winner, loser, winner_score, loser_score, year, month, day):
        self.winner = winner
        self.loser = loser
        self.winner_score = float(winner_score)
        self.loser_score = float(loser_score)
        self.score_diff = self.winner_score - self.loser_score
        self.date = datetime(int(year), int(month), int(day))

def sum_edge_chain(edge_chain, final_date):
    tot = 0.
    for e in edge_chain:
        days = (e.date - final_date).days
        tot += (e.winner_score/len(edge_chain)) * (.90)**days
    return(tot)





