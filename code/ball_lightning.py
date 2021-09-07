from graph_node import graph_node
import sys
import random

if __name__ == "__main__":

    def get_edge_chain(edge_chain, edge_chain_diff, visited_nodes, node, target_id):

        # if we've hit the target return the chain of jumps
        if node.node_id == target_id:
            return(edge_chain, edge_chain_diff)

        else:

            # eliminate already checked nodes
            nodes_to_check = []
            scores = []
            for e in node.edges:
                n = e[1]
                s = int(e[2])
                if n not in visited_nodes:
                    nodes_to_check.append(n)
                    scores.append(s)

            # if all out edges are checked, just return
            if len(nodes_to_check) == 0:
                return([], 0)

            else:
                j = random.randint(0, len(nodes_to_check) - 1)
                r = nodes_to_check[j]
                sc = scores[j]
                edge_chain.append(r)
                edge_chain_diff += sc
                visited_nodes.add(r)
                next_node = nodes[r]
                return(get_edge_chain(edge_chain, edge_chain_diff, visited_nodes, next_node, target_id))

    random.seed(11)
    game_record_file = open(sys.argv[1], 'r')

    nodes = {}
    node_ids = set()
    edges = {}

    # build the graph in memory
    for e in game_record_file:
        winner, loser, score_diff = e.rstrip().split("\t")
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
 
        winner_edge = (winner, loser, int(score_diff))
        #loser_edge = (loser, winner, -int(score_diff))

        nodes[winner].edges.append(winner_edge)
        #nodes[loser].edges.append(loser_edge)

    bracket = open(sys.argv[2], 'r').readlines()
    next_round = []
    longest_overall = []

    while len(bracket) > 1:
        for b in range(int(len(bracket)/2)):

            s1 = bracket[2 * b].rstrip()
            s2 = bracket[2 * b + 1].rstrip()

            win_paths_1 = 0
            weighted_1 = 0.
            longest_path_1 = 0
            total_point_diff_1 = 0
            for i in range(10000):
                edge_list, diff = get_edge_chain([s1], 0, set(s1), nodes[s1], s2)
                if len(edge_list) > len(longest_overall):
                    longest_overall = edge_list
                if len(edge_list) > 1:
                    #print(edge_list)
                    win_paths_1 += 1
                    weighted_1 += 1.0/(len(edge_list))
                    if len(edge_list) > longest_path_1:
                        longest_path_1 = len(edge_list)
                    total_point_diff_1 += diff


            win_paths_2 = 0
            weighted_2 = 0.
            longest_path_2 = 0
            total_point_diff_2 = 0
            for i in range(10000):
                edge_list, diff = get_edge_chain([s2], 0, set(s2), nodes[s2], s1)

                if len(edge_list) > len(longest_overall):
                    longest_overall = edge_list
                if len(edge_list) > 1:
                    #print(edge_list)
                    win_paths_2 += 1
                    weighted_2 += 1.0/(len(edge_list))
                    if len(edge_list) > longest_path_2:
                        longest_path_2 = len(edge_list)
                    total_point_diff_2 += diff

            """
            if win_paths_1 > win_paths_2:
                winner = s1
            elif win_paths_2 > win_paths_1:
                winner = s2
            else:
                winner = [s1, s2][random.randint(0, 1)]

            """
            if longest_path_1 > longest_path_2:
                winner = s1
            elif longest_path_2 > longest_path_1:
                winner = s2
            else:
                winner = [s1, s2][random.randint(0, 1)]

            next_round.append(winner)

            print("{}\t{}\t{}\t{}\t\t{}\t{}".format(winner, longest_path_1, longest_path_2, win_paths_1, win_paths_2, weighted_1, weighted_2))

        bracket = [] + next_round
        next_round = []
    print(len(longest_overall))
    print(longest_overall)

