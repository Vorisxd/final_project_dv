import duckdb
from connector import connect_to_duckdb
from etl import execute_sql_file, insert_df_to_duckdb
from df_setup import *
# По очредно создаем и заполняем данными таблицы

execute_sql_file('new_duck.db','queries/table_creation/Country_tq.sql')
insert_df_to_duckdb(country,'new_duck.db','country')

execute_sql_file('new_duck.db', 'queries/table_creation/League_tq.sql')
insert_df_to_duckdb(league,'new_duck.db','league')

execute_sql_file('new_duck.db', 'queries/table_creation/Player_tq.sql')
insert_df_to_duckdb(player, 'new_duck.db', 'player')

execute_sql_file('new_duck.db', 'queries/table_creation/Player_Attribute_tq.sql')
insert_df_to_duckdb(player_attributes,'new_duck.db', 'player_attributes')

execute_sql_file('new_duck.db', 'queries/table_creation/Team_tq.sql')
insert_df_to_duckdb(team, 'new_duck.db', 'team')

execute_sql_file('new_duck.db', 'queries/table_creation/Match_tq.sql')
insert_df_to_duckdb(match, 'new_duck.db', 'match')

execute_sql_file('new_duck.db', 'queries/view_creation/player_tbl_wq.sql')
execute_sql_file('new_duck.db', 'queries/view_creation/matches_wq.sql')

