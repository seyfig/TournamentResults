#!/usr/bin/env python
# -*- coding: cp1254 -*-
#
# Test cases for tournament.py

from tournament import *
import math
from random import randint

def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testPairings():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."

def testOneRound():
    deleteMatches()
    deletePlayers()
    register42Players()
    playersCount = countPlayers()
    standings = playerStandings()
    players = [row[0] for row in standings]
    i = 0
    while (i < playersCount):
        reportMatch(players[i],players[i+1])
        i = i + 2
    pairings = swissPairingsPreventRematch()
    countMisMatches = 0 
    if len(pairings) != playersCount/2:
        raise ValueError(
            "For %s players, swissPairings should return %s pairs. Not %s" %(playersCount,playersCount/2,len(pairings)))
    for pairing in pairings:
        [pid1, pname1, pid2, pname2,prank1,prank2,pwins1,pwins2,pmatchedBefore] = pairing
        if(pwins1 != pwins2):
            countMisMatches = countMisMatches + 1
            if(countMisMatches > 1):
                raise ValueError("More then 1 mismatches exists. Player %s has %s wins, player %s has %s wins!"%( pid1,pwins1,pid2,pwins2))
    print "9. After one match, players with one win are paired, except %s." %(countMisMatches)

def testTournamentPreventRematch():
    deleteMatches()
    deletePlayers()
    register100Players()
    playersCount = countPlayers()
    rounds = int(math.ceil(math.log(playersCount,2)))
    print "Prevent Rematch, players count: %s, rounds: %s " %(playersCount, rounds)
    for r in range(rounds):
        pairings = swissPairingsPreventRematch()
        countMisMatches = 0 
        if len(pairings) != playersCount/2:
            raise ValueError(
                "For %s players, swissPairings should return %s pairs. Not %s" %(playersCount,playersCount/2,len(pairings)))
        for pairing in pairings:
            [pid1, pname1, pid2, pname2,prank1,prank2,pwins1,pwins2,pmatchedBefore] = pairing
            if(pwins1 != pwins2):
                countMisMatches = countMisMatches + 1
            reportMatch(pid1,pid2)
        if(countMisMatches > r + 1):
            raise ValueError("MisMatches for round %s is %s" %(r + 1, countMisMatches ))
    print "10. After %s rounds, players with one win are paired, except %s." %(rounds,countMisMatches)

def testTournamentOdd():
    deleteMatches()
    deletePlayers()
    register99Players()
    playersCount = countPlayers()
    rounds = int(math.ceil(math.log(playersCount,2)))
    print "Odd number of players, players count: %s, rounds: %s " %(playersCount, rounds)
    for r in range(rounds):
        pairings = swissPairingsPreventRematch()
        countMisMatches = 0 
        if ((len(pairings) < playersCount/2) or (len(pairings) > (playersCount / 2) + 1)):
            raise ValueError(
                "For %s players, swissPairings should return %s or %s pairs. Not %s" %(playersCount,playersCount/2,playersCount/2+1,len(pairings)))
        for pairing in pairings:
            [pid1, pname1, pid2, pname2,prank1,prank2,pwins1,pwins2,pmatchedBefore] = pairing
            if(pwins1 != pwins2):
                countMisMatches = countMisMatches + 1
            reportMatch(pid1,pid2)
        if(countMisMatches > r + 1):
            raise ValueError("MisMatches for round %s is %s" %(r + 1, countMisMatches ))
    print "11. After %s rounds, players with one win are paired, except %s." %(rounds,countMisMatches)

def testTournamentDraw():
    deleteMatches()
    deletePlayers()
    register99Players()
    playersCount = countPlayers()
    rounds = int(math.ceil(math.log(playersCount,2)))
    print "With Draw, players count: %s, rounds: %s " %(playersCount, rounds)
    for r in range(rounds):
        pairings = swissPairingsDraw()
        countMisMatches = 0 
        if ((len(pairings) < playersCount/2) or (len(pairings) > (playersCount / 2) + 1)):
            raise ValueError(
                "For %s players, swissPairings should return %s or %s pairs. Not %s" %(playersCount,playersCount/2,playersCount/2+1,len(pairings)))
        for pairing in pairings:
            [pid1, pname1, pid2, pname2,prank1,prank2,pwins1,pwins2,pmatchedBefore] = pairing
            if(pwins1 != pwins2):
                countMisMatches = countMisMatches + 1
            result = randint(0,2)
            reportMatchWithDraw(pid1,pid2,result)
    print "12. After %s rounds, players with one win are paired, except %s." %(rounds,countMisMatches)

def testTournamentOMW():
    deleteMatches()
    deletePlayers()
    register99Players()
    playersCount = countPlayers()
    rounds = int(math.ceil(math.log(playersCount,2)))
    print "OMW ranking, players count: %s, rounds: %s " %(playersCount, rounds)
    for r in range(rounds):
        pairings = swissPairingsOMW()
        countMisMatches = 0 
        if ((len(pairings) < playersCount/2) or (len(pairings) > (playersCount / 2) + 1)):
            raise ValueError(
                "For %s players, swissPairings should return %s or %s pairs. Not %s" %(playersCount,playersCount/2,playersCount/2+1,len(pairings)))
        for pairing in pairings:
            [pid1, pname1, pid2, pname2,prank1,prank2,pwins1,pwins2,pmatchedBefore] = pairing
            if(pwins1 != pwins2):
                countMisMatches = countMisMatches + 1
            reportMatch(pid1,pid2)
        if(countMisMatches > r + 1):
            raise ValueError("MisMatches for round %s is %s" %(r + 1, countMisMatches ))
    print "13. After %s rounds, players with one win are paired, except %s." %(rounds,countMisMatches)

def testMultipleTournaments():
    deleteMatches()
    deleteTournamentMatches()
    deletePlayerTournaments()
    deleteTournaments()
    deletePlayers()
    register99Players()
    totalPlayers = countPlayers()
    #how many tournaments to test
    tournamentsCount = randint(2,5)
    print "Multiple Tournaments: %s" %(tournamentsCount)
    for t in range(tournamentsCount):
        registerTournament(t,"Tournament " + str(t+1))
        #number of players in the tournament
        playersCount = randint(1,totalPlayers)
        players = playerStandings()
        #register players for the tournament t
        for p in range(playersCount):
            registerPlayerTournament(players[p][0],t)
        rounds = int(math.ceil(math.log(playersCount,2)))
        print "tournament: " + str(t), "Number of players: " + str(playersCount), "Rounds: " + str(rounds)
        for r in range(rounds):
            pairings = swissPairingsMT(t)
            countMisMatches = 0 
            if ((len(pairings) < playersCount/2) or (len(pairings) > (playersCount / 2) + 1)):
                raise ValueError(
                    "For %s players, swissPairings should return %s or %s pairs. Not %s" %(playersCount,playersCount/2,playersCount/2+1,len(pairings)))
            for pairing in pairings:
                [pid1, pname1, pid2, pname2,prank1,prank2,pwins1,pwins2,pmatchedBefore,ptournament] = pairing
                if(pwins1 != pwins2):
                    countMisMatches = countMisMatches + 1
                result = randint(0,2)
                reportMatchTournamentWithDraw(t,pid1,pid2,result)
        print "14. After %s rounds, players with one win are paired, except %s." %(rounds,countMisMatches)
    
def register42Players():
    registerPlayer("Shelia Cohen")
    registerPlayer("Enola Holle")
    registerPlayer("Georgia Conant")
    registerPlayer("Telma Worster")
    registerPlayer("Soledad Romig")
    registerPlayer("Elouise Tobin")
    registerPlayer("Sharleen Roseborough")
    registerPlayer("Regena Donnellan")
    registerPlayer("Leena Frisbee")
    registerPlayer("Robt Ginther")
    registerPlayer("Nilda Thrush")
    registerPlayer("Nicholas Woodell")
    registerPlayer("Carmel Hieb")
    registerPlayer("Willy Hyder")
    registerPlayer("Alta Mona")
    registerPlayer("Kaila Difranco")
    registerPlayer("Alfredo Hovis")
    registerPlayer("Garnett Troncoso")
    registerPlayer("Kathaleen Seybert")
    registerPlayer("Ronny Artiaga")
    registerPlayer("Elias Lehoux")
    registerPlayer("Chance Ekberg")
    registerPlayer("Fidelia Heindel")
    registerPlayer("Dennis Knaus")
    registerPlayer("Maryland Caddy")
    registerPlayer("Sylvie Furry")
    registerPlayer("Renay Hartzler")
    registerPlayer("Bessie Daughtridge")
    registerPlayer("Kurt Sibrian")
    registerPlayer("Audria Thibodaux")
    registerPlayer("Eugenie Steely")
    registerPlayer("Reginia Synder")
    registerPlayer("Berry Elia")
    registerPlayer("Ricki Loberg")
    registerPlayer("Caroline Manz")
    registerPlayer("Mandi Digiovanni")
    registerPlayer("Bethanie Ostrem")
    registerPlayer("Tressa Holliman")
    registerPlayer("Ericka Roux")
    registerPlayer("Leda Riffe")
    registerPlayer("Werner Bazaldua")
    registerPlayer("Ramonita Halle")


def register99Players():
    register42Players()
    registerPlayer("Arminda Sperling")
    registerPlayer("Lindsey Manna")
    registerPlayer("Margit Fyfe")
    registerPlayer("Marquetta Enterline")
    registerPlayer("Pauline Trombetta")
    registerPlayer("Brent Sibert")
    registerPlayer("Numbers Hoback")
    registerPlayer("Lizeth Stodola")
    registerPlayer("Joellen Firth")
    registerPlayer("Elmer Nally")
    registerPlayer("Evie Ho")
    registerPlayer("Ena Tebo")
    registerPlayer("Ezra Nader")
    registerPlayer("Franchesca Stoll")
    registerPlayer("Clair Reams")
    registerPlayer("Lewis Hasse")
    registerPlayer("John Damm")
    registerPlayer("Alanna Schlenker")
    registerPlayer("Rueben Dansereau")
    registerPlayer("Marcelo Clore")
    registerPlayer("Leola Bently")
    registerPlayer("Verlene Calfee")
    registerPlayer("Shiela Keaton")
    registerPlayer("Reena Bonner")
    registerPlayer("Alessandra Fortuna")
    registerPlayer("Cedric Mcnabb")
    registerPlayer("Dee Shillings")
    registerPlayer("Clara Bengston")
    registerPlayer("Jenee Reamer")
    registerPlayer("Voncile Beller")
    registerPlayer("Renato Creagh")
    registerPlayer("Ahmed Greenawalt")
    registerPlayer("Candyce Lui")
    registerPlayer("Britney Voyles")
    registerPlayer("Mee Kellough")
    registerPlayer("Cesar Ogden")
    registerPlayer("Norah Decastro")
    registerPlayer("Chantal Flaherty")
    registerPlayer("Bertram Ruelas")
    registerPlayer("Silas Andreotti")
    registerPlayer("Hulda Smithers")
    registerPlayer("Marnie Quincy")
    registerPlayer("Divina Eddins")
    registerPlayer("Olevia Tillson")
    registerPlayer("Gerri Commodore")
    registerPlayer("Kelsey Boydstun")
    registerPlayer("Julie Woolwine")
    registerPlayer("Merna Coniglio")
    registerPlayer("Kay Runner")
    registerPlayer("Keesha Ravenell")
    registerPlayer("Maureen Wooding")
    registerPlayer("Morgan Kunkle")
    registerPlayer("Fiona Harkleroad")
    registerPlayer("Isreal Santi")
    registerPlayer("Meaghan Naylor")
    registerPlayer("Reginald Clifton")
    registerPlayer("Brigitte Malave")
    
def register100Players():
    register99Players()
    registerPlayer("Nilsa Sheffield")


if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    testOneRound()
    testTournamentPreventRematch()
    testTournamentOdd()
    testTournamentDraw()
    testTournamentOMW()
    testMultipleTournaments()
    print "Success!  All tests pass!"


