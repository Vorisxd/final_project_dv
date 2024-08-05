CREATE VIEW IF NOT EXISTS players_view AS
    SELECT 
        pa.player_api_id,
        p.player_name AS player_name,
        p.birthday AS player_birthday,
        p.height AS player_height,
        p.weight AS player_weight,
        pa.date,
        pa.overall_rating,
        pa.potential,
        pa.preferred_foot,
        pa.attacking_work_rate,
        pa.defensive_work_rate,
        pa.crossing,
        pa.finishing,
        pa.heading_accuracy,
        pa.short_passing,
        pa.volleys,
        pa.dribbling,
        pa.curve
    FROM player_attributes AS pa
    JOIN player p ON pa.player_api_id = p.player_api_id

