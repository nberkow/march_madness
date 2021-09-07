### NCAA Ball Lightning
# A purposfully silly algorithm for filling out a NCAA Basketball Tournament bracket

- Conststruct a directed graph of all teams
- Parse the season records to get win/loss records
- An edge from Node A to Node B means team A beat team B in a game
- Many edges may connect two nodes
- To predict a winner: 
-- Start at Node A and randomly discover paths to Node B
-- Start at B and find paths to A
-- The team with the longest path wins

I made a bracket in 2019, but it didn't win

# Input data from here
https://github.com/lbenz730/NCAA_Hoops/blob/master/3.0_Files/Results/2018-19/NCAA_Hoops_Results_3_9_2019.csv

