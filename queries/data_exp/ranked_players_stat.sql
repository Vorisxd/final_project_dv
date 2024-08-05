WITH ranked_players_stats AS(
    SELECT
        player_api_id,
        player_name,
        player_birthday,
        round(player_height*1, 2) as player_height_cm,
        round(player_weight*0.453, 2) as player_weight_kg,
        date,
        extract(year from age(current_date, player_birthday)) as age_now,
        ROW_NUMBER() OVER (PARTITION BY player_api_id ORDER BY date DESC) AS rn,
        overall_rating,
        potential,
        crossing,
        finishing,
        heading_accuracy,
        short_passing,
        volleys,
        dribbling,
        curve,
        preferred_foot,
        attacking_work_rate,
        defensive_work_rate
    FROM players_view
)
SELECT*
FROM ranked_players_stats
WHERE rn=1