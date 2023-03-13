# Two algorithms for predicting the result of an NCAA tournamet:

## NCAA Ball Lightning
### A purposfully silly algorithm for filling out a NCAA Basketball Tournament bracket

* Conststruct a directed graph of all teams
* Parse the season records to get win/loss records
* An edge from Node A to Node B means team A beat team B in a game
* The weight of an egde reflects
  * how recent the win was
  * how big the score difference was
  * how different the two teams win records are for the season
* To predict a winner: 
  * randomly find paths from A to B with n tries
  * randomly find paths from B to A with n tries
  * longest most improbable path wins!

  usage: python3 ball_lightning.py seed season_file.txt bracket_file.txt

## NCAA Simulator
### An extremely serious algorithm for imputing and simulating games and predicting a March Madness winner

* Read in the win/loss records for all teams
* Do simulated matchups (ignoring conferences and other real world conventions)
* Teams win or lose based on their score records and the score records of their opponents
* Winning teams are awarded wins with scores based on their actual winning games
* Run the tournament!

usage: python3 ball_lightning.py seed season_file.txt bracket_file.txt

example season and bracket files in test_data
seed = your favorite integer


### Input data from here
https://github.com/lbenz730/NCAA_Hoops/blob/master/3.0_Files/Results/

