CREATE TABLE IF NOT EXISTS match(
    id INT NOT NULL,
    country_id INT NOT NULL,
    league_id INT NOT NULL,
    season VARCHAR(10),
    stage INT NOT NULL,
    date TIMESTAMP NOT NULL,
    match_api_id INT NOT NULL,
    home_team_api_id INT NOT NULL,
    away_team_api_id INT NOT NULL,
    home_team_goal INT NOT NULL,
    away_team_goal INT NOT NULL,
    result VARCHAR(10) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (country_id) REFERENCES country(id),
    FOREIGN KEY (league_id) REFERENCES league(id),
    FOREIGN KEY (home_team_api_id) REFERENCES team(team_api_id),
    FOREIGN KEY (away_team_api_id) REFERENCES team(team_api_id)
)