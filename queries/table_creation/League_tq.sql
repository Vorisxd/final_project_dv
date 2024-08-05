CREATE TABLE IF NOT EXISTS league(
    id int NOT NULL,
    country_id INT NOT NULL,
    name VARCHAR (40) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (country_id) REFERENCES country(id)
);
