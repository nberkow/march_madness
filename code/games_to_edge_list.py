import sys

def parse_game(game_line):
    elts = game_line.split(",")
    y, m, d, team, opponent, location, score, opscore, ot, d1 = elts
    te = team[1:-1]
    op = opponent[1:-1]

    if score != 'NA' and opscore != 'NA':
        score = int(score)
        opscore = int(opscore)

        if score >= opscore:
            winner = te
            loser = op
            s = score - opscore
        else:
            winner = op
            loser = te
            s = opscore - score

        return(y, m, d, winner, loser, str(s))
    return(())

if __name__ == "__main__":

    unique_games = set()
    games_file = open(sys.argv[1], 'r')
    games_file.readline()
    for g in games_file:
        game_details = parse_game(g)
        if game_details not in unique_games and game_details != ():
            print("\t".join((game_details[3], game_details[4], game_details[5])))
            unique_games.add(game_details)
        
