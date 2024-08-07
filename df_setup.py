import pandas as pd
#Здесь создаются и редактируются датафреймы для последовательной загрузки данных в бд
#Country df creation
country = pd.read_csv('Source/Csvs/Country.csv')

#League df creation
league = pd.read_csv('Source/Csvs/League.csv')

#match df creation
match = pd.read_csv('Source/Csvs/Match.csv')
match = match.iloc[:,(range(0,11))]
match['result'] = match['home_team_goal']-match['away_team_goal']
match['result'] = match['result'].apply(lambda x: 'win' if x > 0 else ('draw' if x == 0 else 'defeat'))

#player_attributes df creation
player_attributes = pd.read_csv('Source/Csvs/Player_Attributes.csv')
player_attributes.drop('player_fifa_api_id', axis=1, inplace=True)
player_attributes = player_attributes.iloc[:,(range(0,15))]

#player df creation
player = pd.read_csv('Source/Csvs/Player.csv')
player.drop('player_fifa_api_id', axis=1, inplace=True)

#Team Attributes 
team = pd.read_csv('Source/Csvs/Team.csv')
team.drop('team_fifa_api_id', axis=1, inplace=True)



