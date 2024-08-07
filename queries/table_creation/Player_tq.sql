/*Запрос создающий таблицу игроков*/
CREATE TABLE IF NOT EXISTS player(
    id INT NOT NULL,
    player_api_id INT NOT NULL,
    player_name VARCHAR(40) NOT NULL,
    birthday TIMESTAMP NOT NULL,
    height FLOAT NOT NULL,
    weight INT NOT NULL,
    PRIMARY KEY (player_api_id)
)