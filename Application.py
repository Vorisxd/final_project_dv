import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Output, Input
from etl import execute_sql_file
from dash.exceptions import PreventUpdate
import plotly.io as pio
import plotly.subplots as sp
import plotly.graph_objects as go 



# pio.templates.default = "plotly_dark"

clr_= ['rgba(216, 0, 115,1)','rgba(0, 80, 239,1)','rgba(96, 169, 23,1)','rgba(250, 104, 0,1)','rgba(27, 161, 226,1)','rgba(227, 200, 0,1)']
lineClr_ =['rgba(165, 0, 6, 1)','rgba(0, 29, 188, 1)', 'rgba(45, 118, 0, 1)','rgba(199, 53, 0, 1)','rgba(0, 110, 175, 1)', 'rgba(176, 149, 0, 1)']


players = execute_sql_file('new_duck.db','queries/data_exp/players_date.sql',create_df = True)
players_ranked = execute_sql_file('new_duck.db','queries/data_exp/ranked_players_stat.sql',create_df=True)
options = [{'label': c,'value':c} for c in players.player_name.unique()]

attribute_picker_block = dcc.Dropdown(
    id = 'attr_dd',
    options=[
        {'label': c,'value':c} for  c in players.columns.to_list()[6:]
    ],
    value='overall_rating'

)

player_name_picker = dcc.Dropdown(
    id = 'plr_name_dd',
    value='Cristiano Ronaldo'
)



#-------------------------------------------------------------------------------
app = dash.Dash()
server = app.server
app.layout=html.Div(children=[
        html.H1('Ultimate 25k fifa mathes dashboard', 
                style={'font-style':'italic', 
                'font-size':60, 
                'background-color':'orange', 
                'text-align':'center',
                'font-family': 'Roboto, sans-serif'}),
        html.H2('Player Attributes Overview:', 
                style={'font-style':'bold','font-size':30,'font-family': 'Roboto, sans-serif'}),
                
        html.P('This section displays three key visualizations of player attributes, providing insights into different aspects of their performance.',
               style={'font-style':'bold','font-size':20,'font-family': 'Roboto, sans-serif'}),
        html.Div(
            children=[player_name_picker,attribute_picker_block,]
        ),
        dcc.Markdown(id='player-info', style={'fontSize': '18px', 'fontStyle': 'bold', 'font-family': 'Roboto'}),
        html.Div(
            children=[
                dcc.Graph(id='line_fig', style={'width':'50%', 'display':'inline-block'}),
                dcc.Graph(id='bar_fig', style={'width':'50%', 'display':'inline-block'}),
                dcc.Graph(id='pie_plot')
                
            ]
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
        f'**{slctd_plr_name}**, **Age now : {plr_df["age_now"]}, hight: {plr_df["player_height_cm"]}cm, weight: {plr_df["player_weight_kg"]} kg**'
    )

    return player_info
@app.callback(
    Output(component_id='line_fig',component_property='figure'),
    Input(component_id='plr_name_dd', component_property='value'),
    Input(component_id='attr_dd',component_property='value'),
)

def update_line_fig(slctd_plr_name,slctd_attributes):
    
    attribute_filter = 'overall_rating'
    plr_df= players.copy(deep = True)

    
    
    if slctd_plr_name:
        player_filter = slctd_plr_name
        plr_df = plr_df.query(f"player_name=='{player_filter}'")
        

    if slctd_attributes:
        attribute_filter = slctd_attributes
        plr_df = plr_df.loc[:,('date', attribute_filter)]

    line_fig = px.line(
        data_frame=plr_df,
        x = 'date',
        y = f'{attribute_filter}', 
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
        plr_df = plr_df.loc[:,('player_name', attribute_filter)].sort_values(attribute_filter,ascending=False).head(15)
    bar_fig = px.bar(
        data_frame=plr_df,
        x =  f'{attribute_filter}',
        y = 'player_name',
        color='player_name'
    )
    return bar_fig


@app.callback(
    Output(component_id='pie_plot', component_property='figure'),
    Input(component_id='plr_name_dd', component_property='value'),
)

def update_pie_plot(slctd_player):
    player_filter = 'Cristiano Ronaldo'
    plr_df= players_ranked.copy(deep = True)

    if slctd_player:
        player_filter = slctd_player
        plr_df = plr_df.query(f"player_name=='{player_filter}'")
        player_attr ={key:value for key, value in zip(plr_df.columns[8:14],plr_df.iloc[0,8:14])}
    
    pie_plot = sp.make_subplots(rows=1, cols=len(player_attr), subplot_titles=list(player_attr.keys()), specs=[[{'type': 'domain'}] * len(player_attr)])
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
        title_text='Player Attributes',
        annotations=[dict(text=f'{key}<br>{value}', x=0.07+(i*0.172), y=0.42,  font=dict(size=15, color=clr_[i], family='Verdana', weight='bold'), showarrow=False) for i, (key, value) in enumerate(player_attr.items())]
    )

    return pie_plot





if __name__ == '__main__':
    app.run_server(debug=True,)
