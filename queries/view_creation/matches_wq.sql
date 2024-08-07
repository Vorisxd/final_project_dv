/*Запрос создаёт представление из таблиц match, country, league, team*/
CREATE VIEW mathces_v as 
    SELECT
        c.name as country,
        l.name as league,
        m.season as league_season,
        ht.team_long_name AS home_team_name,
        awt.team_long_name AS away_team_name,
        m.home_team_goal,
        m.away_team_goal,
        m.result
    FROM match m
    JOIN country c ON c.id = m.country_id
    JOIN league l ON l.id = m.league_id
    JOIN team ht ON ht.team_api_id = m.home_team_api_id
    JOIN team awt ON awt.team_api_id = m.away_team_api_id;
