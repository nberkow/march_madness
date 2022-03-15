from graph_tools import *
import sys
import random
from datetime import datetime

if __name__ == "__main__":

    def traverse_edges(starting_node, target_id, max_traversal_len, nodes):

        used_edges = set()
        edge_chain = []
        edges_to_follow = starting_node.edges
        i = 0
        j = random.randint(0, len(edges_to_follow) - 1)
        r = edges_to_follow[j]
        used_edges.add(r)
        i += 1

        keep_going = True
        while keep_going:
            node = nodes[r.loser]
            if node.node_id == target_id:
                return(edge_chain)

            edges_to_follow = []
            for e in node.edges:
                if e not in used_edges:
                    edges_to_follow.append(e)
                    
            if len(edges_to_follow) == 0 or i > max_traversal_len:
                keep_going = False
                return([])

            else:
                j = random.randint(0, len(edges_to_follow) - 1)
                r = edges_to_follow[j]
                used_edges.add(r)
                edge_chain.append(r)


    random.seed(11)
    game_record_file = open(sys.argv[1], 'r')

    nodes = {}
    node_ids = set()
    edges = {}

    # build the graph in memory
    game_record_file.readline()
    for e in game_record_file:
        year, month, day, team, opponent, location, teamscore, oppscore, canceled, postponed, ot, d1 = e.rstrip().split(",")
        team = team[1:-1]
        opponent = opponent[1:-1]

        if teamscore != 'NA' and oppscore != 'NA':

            ts = int(teamscore)
            os = int(oppscore)

            if ts > os:
                winner = team
                loser = opponent
                winner_score = teamscore
                loser_score = oppscore

            else:
                winner = opponent
                loser = team
                winner_score = oppscore
                loser_score = teamscore

            if not winner in node_ids:
                winner_node = graph_node()
                winner_node.node_id = winner
                nodes[winner] = winner_node
                node_ids.add(winner)

            if not loser in node_ids:
                loser_node = graph_node()
                loser_node.node_id = loser
                nodes[loser] = loser_node
                node_ids.add(loser)
    
            winner_edge = graph_edge(winner, loser, winner_score, loser_score, year, month, day)
            nodes[winner].edges.append(winner_edge)

    bracket = open(sys.argv[2], 'r').readlines()
    next_round = []
    longest_overall = []
    final_date = datetime(2022, 9, 3)

    while len(bracket) > 1:
        for b in range(int(len(bracket)/2)):

            s1 = bracket[2 * b].rstrip()
            s2 = bracket[2 * b + 1].rstrip()

            win_paths_1 = 0
            weighted_1 = 0.
            best_points_1 = 0.
            longest_path_1 = 0
            total_point_diff_1 = 0
            edge_list_scores_1 = []
            for i in range(10000):
                edge_list = traverse_edges(nodes[s1], s2, 100000, nodes)
                if len(edge_list) > len(longest_overall):
                    longest_overall = edge_list
                if len(edge_list) > 1:
                    win_paths_1 += 1
                    weighted_1 += 1.0/(len(edge_list))
                    if len(edge_list) > longest_path_1:
                        longest_path_1 = len(edge_list)
                    #total_point_diff_1 += diff
                    ec_sum_1 = sum_edge_chain(edge_list, final_date)
                    edge_list_scores_1.append(ec_sum_1)


            win_paths_2 = 0
            weighted_2 = 0.
            best_points_2 = 0.
            longest_path_2 = 0
            total_point_diff_2 = 0
            edge_list_scores_2 = []
            for i in range(10000):
                edge_list = traverse_edges(nodes[s2], s1, 100000, nodes)

                if len(edge_list) > len(longest_overall):
                    longest_overall = edge_list
                if len(edge_list) > 1:
                    win_paths_2 += 1
                    weighted_2 += 1.0/(len(edge_list))
                    if len(edge_list) > longest_path_2:
                        longest_path_2 = len(edge_list)
                    #total_point_diff_2 += diff
                    ec_sum_2 = sum_edge_chain(edge_list, final_date)
                    edge_list_scores_2.append(ec_sum_2)

            if len(edge_list_scores_1) == 0:
                a1 = 0
            else:
                a1 = sum(edge_list_scores_1)/len(edge_list_scores_1)

            if len(edge_list_scores_2) == 0:
                a2 = 0
            else:
                a2 = sum(edge_list_scores_2)/len(edge_list_scores_2)

            if a1 > a2:
                winner = s1
            elif a2 > a1:
                winner = s2
            else:
                winner = [s1, s2][random.randint(0, 1)]

            next_round.append(winner)

            print(f"{winner}\t{a1}\t{a2}")

        bracket = [] + next_round
        next_round = []

