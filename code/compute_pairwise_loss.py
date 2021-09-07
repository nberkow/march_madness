import sys

if __name__ == "__main__":

    summary = {}
    res_file = open(sys.argv[1], 'r')
    res_file.readline()

    for r in res_file:
        elts = r.rstrip().split(",")
        t1 = elts[3][1:-1]
        t2 = elts[4][1:-1]
        games_counted = set()

        if elts[6] == 'NA' or elts[7] == 'NA':
            pass

        else:
            t1_s = int(elts[6])
            t2_s = int(elts[7])

            winner = 'NA'
            loser = 'NA'

            if t1_s > t2_s:
                winner = t1
                loser = t2

            elif t2_s > t1_s:
                winner = t2
                loser = t1

            game_details = (elts[0], elts[1], elts[2], winner, loser)

            if winner != 'NA' and loser != 'NA' and game_details not in games_counted:
                games_counted.add(game_details)
                if not (winner, loser) in summary:
                    summary[(winner, loser)] = {}
                    summary[(winner, loser)]['games'] = 0
                    summary[(winner, loser)]['wins'] = 0

                    summary[(loser, winner)] = {}
                    summary[(loser, winner)]['games'] = 0
                    summary[(loser, winner)]['wins'] = 0
 
                summary[(winner, loser)]['games'] += 1
                summary[(loser, winner)]['games'] += 1
                summary[(winner, loser)]['wins'] += 1

    for s in summary:
        print("{}\t{}\t{}".format(s[0], s[1], float(summary[s]['games'] - summary[s]['wins'])/summary[s]['games'])) 
  
