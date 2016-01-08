#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def getDbAndCursor():
    """Returns a database connection and cursor."""
    db = connect()
    return (db, db.cursor())


def deleteMatches():
    """Remove all the match records from the database."""
    (db, cursor) = getDbAndCursor()
    cursor.execute("DELETE FROM match_results")
    db.commit()


def deletePlayers():
    """Remove all the player records from the database."""
    (db, cursor) = getDbAndCursor()
    cursor.execute("DELETE FROM players")
    db.commit()


def countPlayers():
    """Returns the number of players currently registered."""
    cursor = getDbAndCursor()[1]
    cursor.execute("SELECT COUNT(*) FROM players")
    return cursor.fetchall()[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    (db, cursor) = getDbAndCursor()
    cursor.execute("INSERT INTO players (name) VALUES (%s)",
        (str(bleach.clean(name)),))
    db.commit()


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
    cursor = getDbAndCursor()[1]
    cursor.execute("SELECT * FROM player_standings")
    return cursor.fetchall()


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost

    """
    (db, cursor) = getDbAndCursor()
    cursor.execute("SELECT COALESCE(MAX(round_number), 0) FROM match_results")
    last_round = cursor.fetchall()[0][0]
    new_round = last_round + 1
    cursor.execute("INSERT INTO match_results"
                       "(player_id, round_number, opponent_id, won_round)"
                       "VALUES (%s, %s, %s, TRUE), (%s, %s, %s, FALSE)",
                       (winner, new_round, loser, loser, new_round, winner))
    db.commit()

 
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
    standings = playerStandings()
    players = [record[:2] for record in standings]
    return [p1 + p2 for p1, p2 in zip(players[0::2], players[1::2])]
