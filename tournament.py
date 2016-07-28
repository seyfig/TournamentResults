#!/usr/bin/env python
# -*- coding: cp1254 -*-
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cursor = db.cursor()
    query = "DELETE FROM matches"
    cursor.execute(query)
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cursor = db.cursor()
    query = "DELETE FROM players"
    cursor.execute(query)
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cursor = db.cursor()
    query = "SELECT COUNT(id) FROM players"
    cursor.execute(query)
    playerCount = cursor.fetchall()
    db.close()
    return int(playerCount[0][0])

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cursor = db.cursor()
    query = "INSERT INTO players (name) values(%s)"
    cursor.execute(query,(name,))
    db.commit()
    db.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    cursor = db.cursor()
    query = "SELECT * FROM playerStandings"
    cursor.execute(query)
    standings = cursor.fetchall()
    db.close()
    return standings

def playerStandingsOMW():
    """Returns a list of the players and their win records, sorted by wins and then by OMW.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        OMW: the total number of wins by players they have played against.
        matches: the number of matches the player has played
    """
    db = connect()
    cursor = db.cursor()
    query = "SELECT * FROM playerStandingsOMW"
    cursor.execute(query)
    standings = cursor.fetchall()
    db.close()
    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost

      loser may be null, if it is null, winner will be assigned a "bye".
      Only the last player in the rankings can be in this situation.
      This prevents any player from being assigned multiple times,
      until game is over (log2(countPlayers) rounds played.)
    """

    db = connect()
    cursor = db.cursor()
    query = "INSERT INTO matches (player1,player2,winner) VALUES (%s,%s,%s)"
    cursor.execute(query,(winner,loser,winner,))
    db.commit()
    db.close()

def reportMatchWithDraw(player1, player2,result):
    """Records the outcome of a single match between two players.

    Args:
      player1:  the id number of the player who won
      player2:  the id number of the player who lost
      result: if result is 1, player1 won. if result is 2, player 2 won
              if result is 0, draw game

      player2 may be null, if it is null, winner will be assigned a "bye".
      Only the last player in the rankings can be in this situation.
      This prevents any player from being assigned multiple times,
      until game is over (log2(countPlayers) rounds played.)
    """

    db = connect()
    cursor = db.cursor()
    query = "INSERT INTO matches (player1,player2,winner) VALUES (%s,%s,%s)"
    if(result == 1):
        cursor.execute(query,(player1,player2,player1,))
    elif(result == 2):
        cursor.execute(query,(player1,player2,player2,))
    elif(result == 0):
        cursor.execute(query,(player1,player2,None,))
    db.commit()
    db.close()

def reportMatchTournamentWithDraw(tournament,player1, player2,result):
    """Records the outcome of a single match between two players.

    Args:
      player1:  the id number of the player who won
      player2:  the id number of the player who lost
      result: if result is 1, player1 won. if result is 2, player 2 won
              if result is 0, draw game

      player2 may be null, if it is null, winner will be assigned a "bye".
      Only the last player in the rankings can be in this situation.
      This prevents any player from being assigned multiple times,
      until game is over (log2(countPlayers) rounds played.)
    """
    winner = None
    if(result == 1):
        winner = player1
    elif(result == 2):
        winner = player2
    db = connect()
    cursor = db.cursor()
    query = "INSERT INTO tournamentmatches (tournament,player1,player2,winner) VALUES (%s,%s,%s,%s)"
    cursor.execute(query,(tournament,player1,player2,winner,))    
    db.commit()
    db.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    cursor = db.cursor()
    query = "SELECT id1, name1, id2, name2 FROM swissPairings"
    cursor.execute(query)
    swiss = cursor.fetchall()
    db.close()
    return swiss

def swissPairingsPreventRematch():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2,rank1,rank2,wins1,wins2,matchedBefore)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
        rank1: current rank of the first player
        rank2: current rank of the second player
        wins1: current number of wins of the first player
        wins2: current number of wins of the second player
        matchedBefore: is 1 if two players matched before, 0 otherwise

    """
    db = connect()
    cursor = db.cursor()
    query = "SELECT * FROM swissPairings"
    cursor.execute(query)
    swiss = cursor.fetchall()
    pairings = []
    for s in swiss:
        pairings.append(list(s))
    i = 0
    while(i < len(pairings)):
        #if two players in the pairing matched before
        if(pairings[i][8] == 1):
            j = i - 1
            isRematchResolved = False
#perform search on previous pairings:
#if there exists such a pairing that player1 in the pairing j
#has equal winnings with the player1 in the pairing i
#and player2 in the pairing j hase equal winnings with
#player2 in the pairing i
#and player1 in the pairing i never matched with player2 in pairing j
#and player2 in the pairing i never matched with player1 in pairing j
#then switch player2's of pairing i and pairing j
            while(j>0):
                if((pairings[j][7] == pairings[i][7])
                and (not matchedBefore(pairings[i][0],pairings[j][2]))
                and (pairings[j][6] == pairings[i][6])
                and (not matchedBefore(pairings[j][0],pairings[i][0]))):
                    pid2 = pairings[i][2]
                    pname2 = pairings[i][3]
                    prank2 = pairings[i][5]
                    pwins2 = pairings[i][7]
                    pairings[i][2] = pairings[j][2]
                    pairings[i][3] = pairings[j][3]
                    pairings[i][5] = pairings[j][5]
                    pairings[i][7] = pairings[j][7]
                    pairings[j][2] = pid2
                    pairings[j][3] = pname2
                    pairings[j][5] = prank2
                    pairings[j][7] = pwins2
                    pairings[i][8] = 0
                    pairings[j][8] = 0
                    isRematchResolved = True
                    break
                j = j - 1
#if no available pairings found in previous pairings,
#then search for the subsequent pairings
            if(not isRematchResolved):
                j = i + 1
                while(j < len(pairings)):
                    if((pairings[j][7] == pairings[i][7])
                    and (not matchedBefore(pairings[i][0],pairings[j][2]))
                    and (pairings[j][6] == pairings[i][6])
                    and (not matchedBefore(pairings[j][0],pairings[i][0]))):
                        pid2 = pairings[i][2]
                        pname2 = pairings[i][3]
                        prank2 = pairings[i][5]
                        pwins2 = pairings[i][7]
                        pairings[i][2] = pairings[j][2]
                        pairings[i][3] = pairings[j][3]
                        pairings[i][5] = pairings[j][5]
                        pairings[i][7] = pairings[j][7]
                        pairings[j][2] = pid2
                        pairings[j][3] = pname2
                        pairings[j][5] = prank2
                        pairings[j][7] = pwins2
                        pairings[i][8] = 0
                        pairings[j][8] = 0
                        isRematchResolved = True
                        break
                    j = j + 1
        i = i + 1
    db.close()
    swiss = tuple(pairings)
    return swiss

def swissPairingsDraw():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2,rank1,rank2,wins1,wins2,matchedBefore)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
        rank1: current rank of the first player
        rank2: current rank of the second player
        points1: current number of wins of the first player
        points2: current number of wins of the second player
        matchedBefore: is 1 if two players matched before, 0 otherwise

    """
    db = connect()
    cursor = db.cursor()
    query = "SELECT * FROM swissPairingsDraw"
    cursor.execute(query)
    swiss = cursor.fetchall()
    pairings = []
    for s in swiss:
        pairings.append(list(s))
    i = 0
    while(i < len(pairings)):
        #if two players in the pairing matched before
        if(pairings[i][8] == 1):
            j = i - 1
            isRematchResolved = False
#perform search on previous pairings:
#if there exists such a pairing that
#player1 in the pairing i never matched with player2 in pairing j
#and player2 in the pairing i never matched with player1 in pairing j
#then switch player2's of pairing i and pairing j
            while(j>0):
                if((not matchedBefore(pairings[i][0],pairings[j][2]))
                and (not matchedBefore(pairings[j][0],pairings[i][2]))):
                    pid2 = pairings[i][2]
                    pname2 = pairings[i][3]
                    prank2 = pairings[i][5]
                    ppoints2 = pairings[i][7]
                    pairings[i][2] = pairings[j][2]
                    pairings[i][3] = pairings[j][3]
                    pairings[i][5] = pairings[j][5]
                    pairings[i][7] = pairings[j][7]
                    pairings[j][2] = pid2
                    pairings[j][3] = pname2
                    pairings[j][5] = prank2
                    pairings[j][7] = ppoints2
                    pairings[i][8] = 0
                    pairings[j][8] = 0
                    isRematchResolved = True
                    break
                j = j - 1
#if no available pairings found in previous pairings,
#then search for the subsequent pairings
            if(not isRematchResolved):
                j = i + 1
                while(j < len(pairings)):
                    if((not matchedBefore(pairings[i][0],pairings[j][2]))
                    and (not matchedBefore(pairings[j][0],pairings[i][2]))):
                        pid2 = pairings[i][2]
                        pname2 = pairings[i][3]
                        prank2 = pairings[i][5]
                        ppoints2 = pairings[i][7]
                        pairings[i][2] = pairings[j][2]
                        pairings[i][3] = pairings[j][3]
                        pairings[i][5] = pairings[j][5]
                        pairings[i][7] = pairings[j][7]
                        pairings[j][2] = pid2
                        pairings[j][3] = pname2
                        pairings[j][5] = prank2
                        pairings[j][7] = ppoints2
                        pairings[i][8] = 0
                        pairings[j][8] = 0
                        isRematchResolved = True
                        break
                    j = j + 1
        i = i + 1
    db.close()
    swiss = tuple(pairings)
    return swiss


def swissPairingsOMW():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2,rank1,rank2,wins1,wins2,matchedBefore)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
        rank1: current rank of the first player
        rank2: current rank of the second player
        wins1: current number of wins of the first player
        wins2: current number of wins of the second player
        matchedBefore: is 1 if two players matched before, 0 otherwise

    """
    db = connect()
    cursor = db.cursor()
    query = "SELECT * FROM swissPairingsOMW"
    cursor.execute(query)
    swiss = cursor.fetchall()
    pairings = []
    for s in swiss:
        pairings.append(list(s))
    i = 0
    while(i < len(pairings)):
        #if two players in the pairing matched before
        if(pairings[i][8] == 1):
            j = i - 1
            isRematchResolved = False
#perform search on previous pairings:
#if there exists such a pairing that player1 in the pairing j
#has equal winnings with the player1 in the pairing i
#and player2 in the pairing j hase equal winnings with
#player2 in the pairing i
#and player1 in the pairing i never matched with player2 in pairing j
#and player2 in the pairing i never matched with player1 in pairing j
#then switch player2's of pairing i and pairing j
            while(j>0):
                if((pairings[j][7] == pairings[i][7])
                and (not matchedBefore(pairings[i][0],pairings[j][2]))
                and (pairings[j][6] == pairings[i][6])
                and (not matchedBefore(pairings[j][0],pairings[i][0]))):
                    pid2 = pairings[i][2]
                    pname2 = pairings[i][3]
                    prank2 = pairings[i][5]
                    pwins2 = pairings[i][7]
                    pairings[i][2] = pairings[j][2]
                    pairings[i][3] = pairings[j][3]
                    pairings[i][5] = pairings[j][5]
                    pairings[i][7] = pairings[j][7]
                    pairings[j][2] = pid2
                    pairings[j][3] = pname2
                    pairings[j][5] = prank2
                    pairings[j][7] = pwins2
                    pairings[i][8] = 0
                    pairings[j][8] = 0
                    isRematchResolved = True
                    break
                j = j - 1
#if no available pairings found in previous pairings,
#then search for the subsequent pairings
            if(not isRematchResolved):
                j = i + 1
                while(j < len(pairings)):
                    if((pairings[j][7] == pairings[i][7])
                    and (not matchedBefore(pairings[i][0],pairings[j][2]))
                    and (pairings[j][6] == pairings[i][6])
                    and (not matchedBefore(pairings[j][0],pairings[i][0]))):
                        pid2 = pairings[i][2]
                        pname2 = pairings[i][3]
                        prank2 = pairings[i][5]
                        pwins2 = pairings[i][7]
                        pairings[i][2] = pairings[j][2]
                        pairings[i][3] = pairings[j][3]
                        pairings[i][5] = pairings[j][5]
                        pairings[i][7] = pairings[j][7]
                        pairings[j][2] = pid2
                        pairings[j][3] = pname2
                        pairings[j][5] = prank2
                        pairings[j][7] = pwins2
                        pairings[i][8] = 0
                        pairings[j][8] = 0
                        isRematchResolved = True
                        break
                    j = j + 1
        i = i + 1
    db.close()
    swiss = tuple(pairings)
    return swiss

def swissPairingsMT(tournament):
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2,rank1,rank2,wins1,wins2,matchedBefore)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
        rank1: current rank of the first player
        rank2: current rank of the second player
        wins1: current number of wins of the first player
        wins2: current number of wins of the second player
        matchedBefore: is 1 if two players matched before, 0 otherwise

    """
    db = connect()
    cursor = db.cursor()
    query = "SELECT * FROM swissPairingsMT WHERE tournament = %s"
    cursor.execute(query,(tournament,))
    swiss = cursor.fetchall()
    pairings = []
    for s in swiss:
        pairings.append(list(s))
    i = 0
    while(i < len(pairings)):
        #if two players in the pairing matched before
        if(pairings[i][8] == 1):
            j = i - 1
            isRematchResolved = False
#perform search on previous pairings:
#if there exists such a pairing that player1 in the pairing j
#has equal winnings with the player1 in the pairing i
#and player2 in the pairing j hase equal winnings with
#player2 in the pairing i
#and player1 in the pairing i never matched with player2 in pairing j
#and player2 in the pairing i never matched with player1 in pairing j
#then switch player2's of pairing i and pairing j
            while(j>0):
                if((pairings[j][7] == pairings[i][7])
                and (not matchedTournamentBefore(tournament,pairings[i][0],pairings[j][2]))
                and (pairings[j][6] == pairings[i][6])
                and (not matchedTournamentBefore(tournament,pairings[j][0],pairings[i][0]))):
                    pid2 = pairings[i][2]
                    pname2 = pairings[i][3]
                    prank2 = pairings[i][5]
                    pwins2 = pairings[i][7]
                    pairings[i][2] = pairings[j][2]
                    pairings[i][3] = pairings[j][3]
                    pairings[i][5] = pairings[j][5]
                    pairings[i][7] = pairings[j][7]
                    pairings[j][2] = pid2
                    pairings[j][3] = pname2
                    pairings[j][5] = prank2
                    pairings[j][7] = pwins2
                    pairings[i][8] = 0
                    pairings[j][8] = 0
                    isRematchResolved = True
                    break
                j = j - 1
#if no available pairings found in previous pairings,
#then search for the subsequent pairings
            if(not isRematchResolved):
                j = i + 1
                while(j < len(pairings)):
                    if((pairings[j][7] == pairings[i][7])
                    and (not matchedTournamentBefore(tournament,pairings[i][0],pairings[j][2]))
                    and (pairings[j][6] == pairings[i][6])
                    and (not matchedTournamentBefore(tournament,pairings[j][0],pairings[i][0]))):
                        pid2 = pairings[i][2]
                        pname2 = pairings[i][3]
                        prank2 = pairings[i][5]
                        pwins2 = pairings[i][7]
                        pairings[i][2] = pairings[j][2]
                        pairings[i][3] = pairings[j][3]
                        pairings[i][5] = pairings[j][5]
                        pairings[i][7] = pairings[j][7]
                        pairings[j][2] = pid2
                        pairings[j][3] = pname2
                        pairings[j][5] = prank2
                        pairings[j][7] = pwins2
                        pairings[i][8] = 0
                        pairings[j][8] = 0
                        isRematchResolved = True
                        break
                    j = j + 1
        i = i + 1
    db.close()
    swiss = tuple(pairings)
    return swiss

def matchedBefore(id1,id2):
    """Checks whether two player has matched before.
    Returns true if they mathced before, false otherwise
    """
    db = connect()
    cursor = db.cursor()
    query = "SELECT count(*) FROM matches WHERE (player1 = %s and player2 = %s) or ( player1 = %s and player2 = %s) "
    cursor.execute(query,(id1,id2,id2,id1,))
    mathcesBefore = cursor.fetchall()
    db.close()
    return (int(mathcesBefore[0][0]) > 0)

def matchedTournamentBefore(tournament,id1,id2):
    """Checks whether two player has matched before.
    Returns true if they mathced before, false otherwise
    """
    db = connect()
    cursor = db.cursor()
    query = "SELECT count(*) FROM tournamentmatches WHERE tournament = %s and ((player1 = %s and player2 = %s) or ( player1 = %s and player2 = %s)) "
    cursor.execute(query,(tournament,id1,id2,id2,id1,))
    mathcesBefore = cursor.fetchall()
    db.close()
    return (int(mathcesBefore[0][0]) > 0)

def registerTournament(id,name):
    """Adds a tournament to the tournament database.
  
    Args:
      id: id of the tournament must be unique
      name: the tournament's full name (need not be unique).
    """
    db = connect()
    cursor = db.cursor()
    query = "INSERT INTO tournaments (id,name) values(%s,%s)"
    cursor.execute(query,(id,name,))
    db.commit()
    db.close()

def registerPlayerTournament(player, tournament):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cursor = db.cursor()
    query = "INSERT INTO playertournaments (player,tournament) values(%s,%s)"
    cursor.execute(query,(player, tournament,))
    db.commit()
    db.close()    


def countPlayersTournament(tournament):
    """Returns the number of players currently registered for the tournament."""
    db = connect()
    cursor = db.cursor()
    query = "SELECT COUNT(player) FROM playertournaments where tournament = %s"
    cursor.execute(query,(tournament,))
    playerCount = cursor.fetchall()
    db.close()
    return int(playerCount[0][0])

def deletePlayerTournaments():
    """Remove all the player tournament records from the database."""
    db = connect()
    cursor = db.cursor()
    query = "DELETE FROM playertournaments"
    cursor.execute(query)
    db.commit()
    db.close()

def deleteTournaments():
    """Remove all the player tournament records from the database."""
    db = connect()
    cursor = db.cursor()
    query = "DELETE FROM tournaments"
    cursor.execute(query)
    db.commit()
    db.close()    
    
def deleteTournamentMatches():
    """Remove all the match records from the database."""
    db = connect()
    cursor = db.cursor()
    query = "DELETE FROM tournamentmatches"
    cursor.execute(query)
    db.commit()
    db.close()
