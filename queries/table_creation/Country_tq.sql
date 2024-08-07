/*Запрос создающий таблицу стран*/

CREATE TABLE IF NOT EXISTS country(
    id INT NOT NULL
    ,name VARCHAR(20) NOT NULL
    ,primary key (id)
)