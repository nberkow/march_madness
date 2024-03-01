from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import io
import base64
import plotly.express as px
import plotly.graph_objects as go
from Bracket_Scorer import Bracket_Scorer
import os
from helpers import *

app = Dash(__name__)
server = app.server
data_by_year = index_csvs_by_year([
    "../historical_data/2017_results.csv",
    "../historical_data/2018_results.csv",
    "../historical_data/2019_results.csv",
    "../historical_data/2021_results.csv",
    "../historical_data/2022_results.csv",
    ])
data_by_region = index_by_region(data_by_year)


app.layout = html.Div([
    html.Div([
        dcc.Graph(id="bracket"),
    ], style={'display': 'inline-block', "vertical-align": "top"}),
    html.Div([
        dcc.Dropdown(['East', 'Midwest', 'South', 'West'], value='East', id='region-dropdown'),
        dcc.Dropdown(list(data_by_year.keys()), value='2022', id='year-dropdown'),
    ], style={'width': '20%', 'display': 'inline-block', "vertical-align": "center"})     
])

@app.callback(
    Output('bracket','figure'),
    Input('region-dropdown','value'),
    Input('year-dropdown','value'),
)
def draw_bracket_region_view(region, year):


    t = 0

    layout = go.Layout(
        autosize=False,
        width=900,
        height=700)

    fig = go.Figure(layout=layout)

    matchups = 8
    box_height = 15
    box_width = 70
    matchup_spacing = 35
    teams = data_by_region[year][region]

    x = [0, box_width * 1.2, box_width * 2.2, box_width * 3,]
    i = 0
    t = 0

    while matchups >= 1:
        
        for m in range(matchups):
            team1, team2 = "", ""
            team1, team2 = teams[t]

            matchup_center_y = (m+0.5) * matchup_spacing
            upper_box = get_box_trace(x[i], matchup_center_y + box_height/2, box_height, box_width, team1)
            fig.add_trace(upper_box)

            lower_box = get_box_trace(x[i], matchup_center_y - box_height/2, box_height, box_width, team2)
            fig.add_trace(lower_box)
            t += 1

        matchups = int(matchups/2)
        matchup_spacing = matchup_spacing * 2
        i += 1

    return(fig)


def get_box_trace(center_x, center_y, box_height, box_width, text, fillcolor='white'):

    y_coords = [
        center_y - box_height/2, 
        center_y - box_height/2, # text
        center_y - box_height/2, 
        center_y + box_height/2, 
        center_y + box_height/2,
        center_y - box_height/2, 
    ]

    x_coords = [
        center_x - box_width/2, 
        center_x,                # text 
        center_x + box_width/2, 
        center_x + box_width/2, 
        center_x - box_width/2,
        center_x - box_width/2, 
    ]

    trace = go.Scatter(x=x_coords, y=y_coords, 
        fill="toself", 
        line_color='black', 
        fillcolor='white',
        mode='lines+text', 
        text = [None, text],
        textposition="top center",
        showlegend=False)
       
    return(trace)




if __name__ == '__main__':
    app.run_server(debug=True)