# Tournament Planner


### The Tournament Planner is a Python module, which allows users to do mainly the following:

 * Keep track of players and matches in a game tournament, 
 * Pair players according to the Swiss system
	
### In order to run the module, it is required to:

 * Have Python 2 and PostgreSQL installed,
 * Run tournament.sql from PostgreSQL, in order to initialize the database schema 
 * Import tournament.py
 * To run test, run tournament_test.py
	
### Using tournament.py module:

 * registerPlayer(name)
 * countPlayers()
 * deletePlayers()
 * reportMatch(winner, loser)
 * deleteMatches()
 * playerStandings()
 * swissPairings()
 * playerStandingsOMW()
 * reportMatchWithDraw(player1, player2,result)
 * reportMatchTournamentWithDraw(tournament,player1, player2,result)
 * swissPairingsPreventRematch()
 * swissPairingsDraw()
 * swissPairingsOMW()
 * swissPairingsMT(tournament)
 * matchedBefore(id1,id2)
 * matchedTournamentBefore(tournament,id1,id2)
 * registerTournament(id,name)
 * registerPlayerTournament(player, tournament)
 * countPlayersTournament(tournament)
 * deletePlayerTournaments()
 * deleteTournaments()
 * deleteTournamentMatches()
