-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create DATABASE tournaments
create database tournament;

\c tournament;
-- Create TABLEs Single Tournament
create table players(
	id serial primary key,
	name text
);

create table matches(
	id serial primary key,
	player1 int references players(id),
	player2 int references players(id),
	winner int references players(id)
);

--Create VIEWs for Initial Requirements
create view playerStandings as
select 	players.id, 
		players.name, 
		(select count(matches.winner)
			from matches 
			where players.id = matches.winner) as wins,
		(select count(*)
			from matches 
			where players.id = matches.player1
			   or players.id = matches.player2) as matches
from players
order by wins desc;

create view playerStandingsRank as
select 	row_number() over (ORDER BY wins desc) as rank,
		playerStandings.*
from playerStandings
order by wins desc;

create view swissPairings as 
select 	players1.id as id1,
		players1.name as name1,
		players2.id as id2,
		players2.name as name2,
		players1.rank as rank1,
		players2.rank as rank2,
		players1.wins as win1,
		players2.wins as win2,
		case 	when exists ( select 1 from matches where player1 = players1.id and player2 = players2.id) then 1
				when exists ( select 1 from matches where player1 = players2.id and player2 = players1.id) then 1
				else 0 end as matchedBefore
from playerStandingsRank players1 
left outer join playerStandingsRank players2
  on players1.rank + 1 = players2.rank
  and mod(players2.rank,2) = 0
where mod(players1.rank,2) = 1
 order by rank1;

 --Create VIEWs for Draw Games
create view playerStandingsDraw as
select 	players.id, 
		players.name, 
		(select count(matches.winner)
			from matches 
			where players.id = matches.winner) * 3
		+
		(select count(*)
			from matches 
			where winner is null
			  and (players.id = matches.player1
			   or  players.id = matches.player2)) as points,
		(select count(*)
			from matches 
			where players.id = matches.player1
			   or players.id = matches.player2) as matches
from players
order by points desc;

create view playerStandingsRankDraw as
select 	row_number() over (ORDER BY points desc) as rank,
		playerStandingsDraw.*
from playerStandingsDraw
order by points desc;

create view swissPairingsDraw as 
select 	players1.id as id1,
		players1.name as name1,
		players2.id as id2,
		players2.name as name2,
		players1.rank as rank1,
		players2.rank as rank2,
		players1.points as win1,
		players2.points as win2,
		case 	when exists ( select 1 from matches where player1 = players1.id and player2 = players2.id) then 1
				when exists ( select 1 from matches where player1 = players2.id and player2 = players1.id) then 1
				else 0 end as matchedBefore
from playerStandingsRankDraw players1 
left outer join playerStandingsRankDraw players2
  on players1.rank + 1 = players2.rank
  and mod(players2.rank,2) = 0
where mod(players1.rank,2) = 1
 order by rank1;
 
 --Create VIEWs for OMW
create view playerStandingsOMW as
select 	players.id, 
		players.name, 
		(select count(matches.winner)
			from matches 
			where players.id = matches.winner) as wins,
		(select count(m.winner)
			 from matches m,
			 (select m.player1 as opponentId
			from matches m
			where m.player2 = players.id
			union 
			select m.player2 as opponentId
			from matches m
			where m.player1 = players.id) OM
			 where m.winner = OM.opponentId) as omw,
		(select count(*)
			from matches 
			where players.id = matches.player1
			   or players.id = matches.player2) as matches
from players
order by wins desc, omw desc;

create view playerStandingsRankOMW as
select 	row_number() over (ORDER BY wins desc, OMW desc) as rank,
		playerStandingsOMW.*
from playerStandingsOMW
order by wins desc, OMW desc;

create view swissPairingsOMW as 
select 	players1.id as id1,
		players1.name as name1,
		players2.id as id2,
		players2.name as name2,
		players1.rank as rank1,
		players2.rank as rank2,
		players1.wins as win1,
		players2.wins as win2,
		case 	when exists ( select 1 from matches where player1 = players1.id and player2 = players2.id) then 1
				when exists ( select 1 from matches where player1 = players2.id and player2 = players1.id) then 1
				else 0 end as matchedBefore
from playerStandingsRankOMW players1 
left outer join playerStandingsRankOMW players2
  on players1.rank + 1 = players2.rank
  and mod(players2.rank,2) = 0
where mod(players1.rank,2) = 1
 order by rank1;
 
 -- Create TABLEs Multiple Tournaments
create table tournaments(
	id int primary key,
	name text
);

create table playertournaments(
	id serial primary key,
	player int references players(id),
	tournament int references tournaments(id)
);

create table tournamentmatches(
	id serial primary key,
	tournament int references tournaments(id),
	player1 int references players(id),
	player2 int references players(id),
	winner int references players(id)
);

 --Create VIEWs for Multiple Tournaments
create view playerStandingsMT as
select 	playertournaments.tournament,
		players.id, 
		players.name, 
		(select count(tournamentmatches.winner)
			from tournamentmatches 
			where players.id = tournamentmatches.winner
			  and tournamentmatches.tournament = playertournaments.tournament) as wins,
		(select count(m.winner)
			 from tournamentmatches m,
			 (select m.player1 as opponentId
			from tournamentmatches m
			where m.player2 = players.id
			  and m.tournament = playertournaments.tournament
			union 
			select m.player2 as opponentId
			from tournamentmatches m
			where m.player1 = players.id
			  and m.tournament = playertournaments.tournament) OM
			 where m.winner = OM.opponentId) as omw,
		(select count(*)
			from tournamentmatches m
			where m.tournament = playertournaments.tournament
			  and (players.id = m.player1
			   or players.id = m.player2)) as matches
from players
join playertournaments on players.id = playertournaments.player
order by playertournaments.tournament, wins desc, omw desc;

create view playerStandingsRankMT as
select 	row_number() over (PARTITION BY tournament ORDER BY wins desc, OMW desc) as rank,
		playerStandingsMT.*
from playerStandingsMT
order by tournament, wins desc, OMW desc;

create view swissPairingsMT as 
select 	players1.id as id1,
		players1.name as name1,
		players2.id as id2,
		players2.name as name2,
		players1.rank as rank1,
		players2.rank as rank2,
		players1.wins as win1,
		players2.wins as win2,
		case 	when exists ( select 1 from matches where player1 = players1.id and player2 = players2.id) then 1
				when exists ( select 1 from matches where player1 = players2.id and player2 = players1.id) then 1
				else 0 end as matchedBefore,
		players1.tournament
from playerStandingsRankMT players1 
left outer join playerStandingsRankMT players2
  on players1.rank + 1 = players2.rank
  and mod(players2.rank,2) = 0
  and players1.tournament = players2.tournament
where mod(players1.rank,2) = 1
 order by rank1;