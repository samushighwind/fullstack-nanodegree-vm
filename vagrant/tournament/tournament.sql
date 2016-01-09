-- Table and view definitions for the tournament project.

-- Create database

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

\connect tournament;


-- Create tables

CREATE TABLE players (
    name TEXT NOT NULL,
    id SERIAL PRIMARY KEY NOT NULL
);

-- Two entries are stored for each match, one for each
-- player involved. While this schema takes up twice as
-- many rows, it simplifies the assurance that no more
-- than one match per player is recorded, per round.
CREATE TABLE match_results (
    player_id INTEGER NOT NULL REFERENCES players (id),
    round_number INTEGER NOT NULL,
    opponent_id INTEGER NOT NULL REFERENCES players (id),
    won_round BOOLEAN NOT NULL,
    PRIMARY KEY (player_id, round_number)
);


-- Create views

CREATE VIEW player_standings AS
    SELECT players.id AS id,
           name,
           COALESCE(wins, 0) AS wins,
           COALESCE(matches, 0) AS matches
    FROM players
    LEFT JOIN ( SELECT match_totals.player_id AS id,
                       matches,
                       COALESCE(wins, 0) AS wins
                FROM ( SELECT player_id, COUNT(*) AS wins
                       FROM match_results
                       WHERE won_round = TRUE
                       GROUP BY player_id ) as win_totals
                RIGHT JOIN ( SELECT player_id, COUNT(*) AS matches
                             FROM match_results
                             GROUP BY player_id ) as match_totals
                ON match_totals.player_id = win_totals.player_id ) AS stats
    ON players.id = stats.id
    ORDER BY wins DESC;
