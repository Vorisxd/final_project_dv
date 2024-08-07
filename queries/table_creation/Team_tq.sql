/*Запрос создающий команды*/
CREATE TABLE IF NOT EXISTS team(
    id INT NOT NULL,
    team_api_id INT NOT NULL,
    team_long_name VARCHAR(25),
    team_short_name VARCHAR(10),
    PRIMARY KEY (team_api_id)
)


