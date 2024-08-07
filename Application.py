import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Output, Input
from etl import execute_sql_file
from dash.exceptions import PreventUpdate
import plotly.subplots as sp
import plotly.graph_objects as go 


#В этой части создаются и редактируются датафреймы для визуализации--------------------------------------------------------
players = execute_sql_file('new_duck.db','queries/data_exp/players_date.sql',create_df = True) #df players
players_ranked = execute_sql_file('new_duck.db','queries/data_exp/ranked_players_stat.sql',create_df=True)#df players_ranked
players_ranked[players_ranked.columns[14:17]] = players_ranked[players_ranked.columns[14:17]].fillna(0)
matches = execute_sql_file('new_duck.db','queries/data_exp/Matchesdata.sql',create_df=True)#df matches


options = [{'label': c,'value':c} for c in players.player_name.unique()]
#Координаты аннотаций к круговой диаграмме
annot_coord_1 = [0.5, 0.225, 0.145, 0.105, 0.085,0.073 ]
annot_coord_2 = [0, 0.55, 0.355, 0.2625,0.2075, 0.172]

#затемнение заднего фона дашьорда
external_stylesheets = ['assets/style.css'] 

#списки с цветами для круговой диаграммы
clr_ = [
    'rgba(255, 165, 0, 1)',  # Яркий оранжевый
    'rgba(255, 255, 0, 1)',   # Яркий желтый
    'rgba(255, 0, 255, 1)',  # Яркий розовый
    'rgba(0, 255, 255, 1)',  # Яркий голубой
    'rgba(0, 255, 0, 1)',    # Яркий зеленый
    'rgba(0, 191, 255, 1)',  # Яркий небесно-голубой
    
]

lineClr_ = [
    'rgba(255, 140, 0, 1)',  # Тёмный оранжевый
    'rgba(204, 204, 0, 1)',   # Тёмный желтый
    'rgba(204, 0, 204, 1)',  # Тёмный розовый
    'rgba(0, 204, 204, 1)',  # Тёмный голубой
    'rgba(0, 204, 0, 1)',    # Тёмный зеленый
    'rgba(0, 153, 204, 1)',  # Тёмный небесно-голубой
    
]




#блок 
attribute_picker_block = dcc.Dropdown(
    id = 'attr_dd',
    options=[
        {'label': c.replace('_',' ').capitalize(),'value':c} for  c in players.columns.to_list()[6:15]
    ],
    multi=True,
    value=['overall_rating']

)

player_name_picker = dcc.Dropdown(
    id = 'plr_name_dd',
    value='Cristiano Ronaldo'
)
#Matches dropdowns----------------------------------------------------------------------------------------------------------------------------------------------------------------
country_dd = dcc.Dropdown(
    id = 'country_dd',
    options=[
        {'label': c,'value':c} for  c in matches['country'].unique()
    ],
)

league_dd = dcc.Dropdown(
    id = 'league_dd',
    options=[
        {'label': c,'value':c} for  c in matches['league'].unique()
    ],
    style={'width':'33%', 'display':'inline-block'}
)

league_season = dcc.Dropdown(
    id = 'league_season_dd',
    options=[
        {'label': c,'value':c} for  c in matches['league_season'].unique()
    ],
    style={'width':'33%', 'display':'inline-block'}
)  

home_team_dd = dcc.Dropdown(
    id = 'home_team_dd',
    options=[
        {'label': c,'value':c} for  c in matches['home_team_name'].unique()
    ],
    style={'width':'33%', 'display':'inline-block'}
)

away_team_dd = dcc.Dropdown(
    id = 'away_team_dd',
    options=[
        {'label': c,'value':c} for  c in matches['away_team_name'].unique()
    ],
)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout=html.Div(
        style={'backgroundColor': '#000000','height': '100vh'},
        children=[
        html.H1('Ultimate 25k fifa mathes dashboard', 
                style={'font-style':'italic', 
                'font-size':60, 
                'background-color':'orange', 
                'text-align':'center',
                'font-family': 'Roboto, sans-serif'},
        ),
        html.H2('Player Attributes Overview:', 
                style={'font-style':'bold','font-size':30,'font-family': 'Roboto, sans-serif','background-color':'orange'}),
                
        html.P('This section displays three key visualizations of player attributes, providing insights into different aspects of their performance.',
               style={'font-style':'bold','font-size':20,'font-family': 'Roboto, sans-serif','color': 'orange'}),
        html.Div(
            children=[player_name_picker,attribute_picker_block,]
        ),
        html.Div(
            children=[
                dcc.Graph(id='line_fig', style={'width':'50%', 'display':'inline-block'}),
                dcc.Graph(id='bar_fig', style={'width':'50%', 'display':'inline-block'}),
                dcc.Markdown(id='player-info', style={'fontSize': '18px', 'fontStyle': 'bold', 'font-family': 'Roboto'}),
                html.H2('Ultimate Player Stats & Comparison', 
                    style={'font-style':'italic', 
                    'font-size':60, 
                    'background-color':'orange', 
                    'text-align':'center',
                    'font-color':'black', 
                    'font-family': 'Roboto, sans-serif'}),
                dcc.Graph(id='pie_plot'),
                dcc.Dropdown(id = 'vs_plr_dd',value='Lionel Messi', options = [{'label': c,'value':c} for c in players_ranked.player_name.unique()], style={'width':'50%', 'display':'inline-block'}),
                dcc.Graph(id = 'vs_bar_fig'),
                html.H1('Ultimate Football Match Dash',
                    style={'font-style':'italic', 
                    'font-size':60, 
                    'background-color':'orange', 
                    'text-align':'center',
                    'font-color':'black', 
                    'font-family': 'Roboto, sans-serif'})]),
        html.Div(
            children=[country_dd,league_dd,league_season,home_team_dd,away_team_dd]),
        html.Div(
            dcc.Graph(id = 'singlepie')
        )
        
    ]
)
#---------------------------------------------------------------------------------

@app.callback(
    Output(component_id='plr_name_dd',component_property='options'),
    Input(component_id='plr_name_dd', component_property='search_value')
)
def update_options(search_value):
    if not search_value:
        raise PreventUpdate
    return [o for o in options if search_value in o["label"]]

@app.callback(
    Output(component_id='player-info', component_property='children'),
    Input(component_id='plr_name_dd', component_property='value'),
)
def update_player_info(slctd_plr_name):
    player_filter = slctd_plr_name
    plr_df = players_ranked.query(f"player_name=='{slctd_plr_name}'").iloc[0]
    player_info = (
        f'''**{slctd_plr_name}**, Age now : **{plr_df["age_now"]},** 
        hight: **{plr_df["player_height_cm"]}cm,** weight: **{plr_df["player_weight_kg"]} kg**, 
        prefered foot: **{plr_df['preferred_foot'].upper()}**, attacking work rate: **{plr_df['attacking_work_rate'].upper()}** 
        defensive work rate: **{plr_df['defensive_work_rate'].upper()}**''' 
    )

    return player_info

#line_fig-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.callback(
    Output(component_id='line_fig',component_property='figure'),
    Input(component_id='plr_name_dd', component_property='value'),
    Input(component_id='attr_dd',component_property='value'),
)

def update_line_fig(slctd_plr_name,slctd_attributes):
    
    attribute_filter = ['overall_rating']
    plr_df= players.copy(deep = True)

    
    
    if slctd_plr_name:
        player_filter = slctd_plr_name
        plr_df = plr_df.query(f"player_name=='{player_filter}'")
        

    if slctd_attributes:
        attribute_filter = slctd_attributes
        plr_df = plr_df.loc[:, ['date'] + attribute_filter]
    line_fig = go.Figure()
    for value in attribute_filter:
        line_fig.add_trace(go.Scatter(x=plr_df['date'], y=plr_df[value], mode='lines+markers', name=value))

    line_fig.update_layout(
        xaxis_title='',
        yaxis_title='', 
        title_text=f'{player_filter}-s stats rate over time'
        ,template='plotly_dark'
    )
        
        
    return line_fig

@app.callback(
    Output(component_id='bar_fig', component_property='figure'),
    Input(component_id='attr_dd', component_property='value'),
)

def update_bar_fig(slctd_attributes):
    attribute_filter = 'overall_rating'
    plr_df= players_ranked.copy(deep = True)
    
    if slctd_attributes:
        attribute_filter = slctd_attributes
        plr_df = plr_df.loc[:,('player_name', attribute_filter[0])].sort_values(attribute_filter[0],ascending=False).head(15)
    bar_fig = px.bar(
        data_frame=plr_df,
        x =  f'{attribute_filter[0]}',
        y = 'player_name',
        color='player_name'
    )

    bar_fig.update_layout(
        xaxis_title='',
        yaxis_title='',
        title_text=f'Top 15 players by {attribute_filter[0]} rate',
        showlegend=False,
        template='plotly_dark'

)
    return bar_fig

#pie_plot--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.callback(
    Output(component_id='pie_plot', component_property='figure'),
    Input(component_id='plr_name_dd', component_property='value'),
    Input(component_id='attr_dd',component_property='value')
)

def update_pie_plot(slctd_player, slctd_attributes):
    player_filter = 'Cristiano Ronaldo'
    attribute_filter = ['overall_rating']
    plr_df= players_ranked.copy(deep = True)

    if slctd_player:
        player_filter = slctd_player
        plr_df = plr_df.query(f"player_name=='{player_filter}'")

    if slctd_attributes:
        attribute_filter = slctd_attributes
        plr_df = plr_df.loc[:,attribute_filter]
        player_attr ={key:value for key, value in zip(plr_df.columns, plr_df.iloc[0,:])}
    pie_plot = sp.make_subplots(rows=1, cols=len(player_attr), subplot_titles=list(player_attr.keys()), specs=[[{'type': 'domain'}] * len(player_attr)])
    if len(attribute_filter)<=6:
        for i, (attribute, value) in enumerate(player_attr.items()):
            pie_plot.add_trace(go.Pie(
                values=[value, 100 - value],
                labels=[attribute, ''],
                hole=0.8,
                textinfo='none',
                showlegend=False,
                marker=dict(
                    colors=[clr_[i], 'rgba(0, 0, 0, 0.01)'],
                    line=dict(color=[lineClr_[i], lineClr_[i]], width=3)),
                rotation=(180 if value > 50 else 0)
            ), 1, i + 1)
    pie_plot.update_layout(
            title_text=f"<b style='color:#ffa500;'>Player statistics out of 100</b>",
            title_font_weight=1000,
            title_x=0.5,
            template='plotly_dark',
    
    annotations=[dict(text=f'{key}<br>{value}', 
                    x=annot_coord_1[len(player_attr)-1]+annot_coord_2[len(player_attr)-1]*i, 
                    y=0.42,  
                    font=dict(size=14, color=clr_[i], 
                    family='Arial', weight=900), 
                    showarrow=False) for i, (key, value) in enumerate(player_attr.items())]
    )

    return pie_plot

#update_vs_bar_fig---------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.callback(
    Output(component_id='vs_bar_fig', component_property='figure'),
    Input(component_id='plr_name_dd', component_property='value'),
    Input(component_id='vs_plr_dd', component_property='value'),    
)

def update_vs_bar_fig(slctd_player, vs_player):
    player_filter = 'Cristiano Ronaldo'
    vs_player_filter = 'Lionel Messi'
    plr_df= players_ranked.iloc[:, [1] + list(range(8, 17))].copy(deep = True)
    plr_df = pd.melt(plr_df, id_vars=['player_name'], var_name='attribute', value_name='value')
    plr_df = plr_df.pivot_table(index=['attribute'], columns=['player_name'], values='value').reset_index()
    
    if slctd_player and vs_player:
        player_filter = slctd_player
        vs_player_filter = vs_player
        plr_df = plr_df.loc[:, ['attribute']+[player_filter,vs_player_filter]]
        plr_df = plr_df.sort_values(plr_df.columns[1]).reset_index()
        
        
    vs_bar_fig = fig = sp.make_subplots(rows=1, cols=2, shared_yaxes=True)
    vs_bar_fig.add_trace(go.Bar(x=plr_df.loc[:,player_filter], y=plr_df.loc[:,'attribute'], orientation='h', name=f'{player_filter}',marker_color='#1aceff'), row=1, col=1)
    vs_bar_fig.add_trace(go.Bar(x=plr_df.loc[:,vs_player_filter], y=plr_df.loc[:,'attribute'], orientation='h', name=f'{vs_player_filter}',marker_color='#ff24e9'), row=1, col=2)
    
    vs_bar_fig.update_xaxes(range=[0, 100],row=1, col=2)
    vs_bar_fig.update_xaxes(range=[100, 0],row=1, col=1)
    vs_bar_fig.update_yaxes(showticklabels=False, row=1, col=1)
    vs_bar_fig.update_yaxes(showticklabels=False, row=1, col=2)
 

    annotations = []
    for i, category in enumerate(plr_df.loc[:,'attribute'].tolist()):
        clr=''
        if plr_df.loc[i,player_filter]>plr_df.loc[i,vs_player_filter]:
            clr='#1aceff'
        elif plr_df.loc[i,player_filter]<plr_df.loc[i,vs_player_filter]:
            clr='#ff24e9'
        else:
            clr='White'
        annotations.append(dict(
            x=0.5,
            y=(len(plr_df.iloc[:,0].tolist()) - (9-i-0.5)) / len(plr_df.iloc[:,0].tolist()),
            xref='paper',
            yref='paper',
            text=category,
            font=dict(size=12, color= clr, family='Arial', weight=900),
            showarrow=False,
            xanchor='center',
            yanchor='middle',
        ))
    vs_bar_fig.update_layout(
        template='plotly_dark',
        title={
        'text': f"<b style='color:#1aceff;'>{player_filter}</b> VS <b style='color:#ff24e9;'>{vs_player_filter}</b>",
        'x': 0.5, 
        'xanchor': 'center'},
        showlegend=False,
        annotations=annotations),
    

    return vs_bar_fig
#Matches callbacks------------------------------------------------------------------------------------------------------------
@app.callback(
    Output('league_dd', 'options'),
    Input('country_dd', 'value')
)
def update_leagues(selected_country):
    if selected_country is None:
        return [{'label': c, 'value': c} for c in matches['league'].unique()]
    filtered_matches = matches[matches['country'] == selected_country]
    return [{'label': c, 'value': c} for c in filtered_matches['league'].unique()]

@app.callback(
    Output('league_season_dd', 'options'),
    Input('league_dd', 'value'),
    Input('country_dd', 'value')
)
def update_league_seasons(selected_league, selected_country):
    if selected_league is None or selected_country is None:
        return [{'label': c, 'value': c} for c in matches['league_season'].unique()]
    filtered_matches = matches[(matches['league'] == selected_league) & (matches['country'] == selected_country)]
    return [{'label': c, 'value': c} for c in filtered_matches['league_season'].unique()]

@app.callback(
    Output('home_team_dd', 'options'),
    Input('league_season_dd', 'value'),
    Input('league_dd', 'value'),
    Input('country_dd', 'value')
)
def update_home_teams(selected_league_season, selected_league, selected_country):
    if selected_league_season is None or selected_league is None or selected_country is None:
        return [{'label': c, 'value': c} for c in matches['home_team_name'].unique()]
    filtered_matches = matches[(matches['league_season'] == selected_league_season) &
                               (matches['league'] == selected_league) &
                               (matches['country'] == selected_country)]
    return [{'label': c, 'value': c} for c in filtered_matches['home_team_name'].unique()]

@app.callback(
    Output('away_team_dd', 'options'),
    Input('home_team_dd', 'value'),
    Input('league_season_dd', 'value'),
    Input('league_dd', 'value'),
    Input('country_dd', 'value')
)
def update_away_teams(selected_home_team, selected_league_season, selected_league, selected_country):
    if selected_home_team is None or selected_league_season is None or selected_league is None or selected_country is None:
        return [{'label': c, 'value': c} for c in matches['away_team_name'].unique()]
    filtered_matches = matches[(matches['home_team_name'] == selected_home_team) &
                               (matches['league_season'] == selected_league_season) &
                               (matches['league'] == selected_league) &
                               (matches['country'] == selected_country)]
    return [{'label': c, 'value': c} for c in filtered_matches['away_team_name'].unique()]

@app.callback(
    Output('singlepie', 'figure'),
    Input('home_team_dd', 'value'),
    Input('league_season_dd', 'value'),
)

def update_singlepie(selected_home_team, selected_league_season):
    filtered_matches = matches.copy(deep=True)
    if selected_home_team and selected_league_season:
        filtered_matches = matches[(matches['home_team_name'] == selected_home_team) &
                                   (matches['league_season'] == selected_league_season)]
    results_count = filtered_matches['result'].value_counts().reset_index()
    results_count.columns = ['result', 'count']
    
    singlepie = px.pie(
        results_count,
        names='result',
        values='count',
        title=f'Results for {selected_home_team} in {selected_league_season}'
    )

    singlepie.update_layout(
        template='plotly_dark')

        
    return singlepie
    





if __name__ == '__main__':
    app.run_server(debug=True,)
