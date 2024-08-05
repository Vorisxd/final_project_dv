CREATE TABLE if NOT EXISTS player_attributes(
    id INT NOT NULL,
    player_api_id INT NOT NULL,
    date TIMESTAMP,
    overall_rating FLOAT,
    potential FLOAT,
    preferred_foot VARCHAR(25),    
    attacking_work_rate  VARCHAR(25), 
    defensive_work_rate  VARCHAR(25), 
    crossing FLOAT,
    finishing FLOAT,
    heading_accuracy FLOAT,          
    short_passing FLOAT,
    volleys FLOAT,
    dribbling FLOAT,
    curve FLOAT,
    FOREIGN KEY (player_api_id) REFERENCES player(player_api_id)
)